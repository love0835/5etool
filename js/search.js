"use strict";

class SearchPage {
	static async pInit () {
		ExcludeUtil.pInitialise(); // don't await, as this is only used for search

		SearchPage._isAllExpanded = (await StorageUtil.pGetForPage(SearchPage._STORAGE_KEY_IS_EXPANDED)) || false;
		SearchPage._$wrp = $(`#main_content`).empty();
		this._render();
	}

	static _render () {
		let isInitialHooks = true;

		Omnisearch.initState();

		const $iptSearch = $(`<input class="form-control pg-search__ipt" placeholder="全域搜索..." title="生命：很有可能搜不到全域的內容。使用時請注意。">`)
			.keydown(evt => {
				if (evt.key !== "Enter") return;
				$btnSearch.click();
			})
			.val(decodeURIComponent(location.search.slice(1).replace(/\+/g, " ")))

		const $btnSearch = $(`<button class="btn btn-default"><span class="glyphicon glyphicon-search"></span></button>`)
			.click(() => {
				location.search = encodeURIComponent($iptSearch.val().trim().toLowerCase());
			});

		const $btnHelp = $(`<button class="btn btn-default mr-2 mobile__hidden" title="幫助"><span class="glyphicon glyphicon-info-sign"></span></button>`)
			.click(() => Omnisearch.doShowHelp());

		const $btnToggleUa = $(`<button class="btn btn-default" title="篩選 UA 和其他非官方資源">包含 UA</button>`)
			.click(() => Omnisearch.doToggleUa());
		const hkUa = () => {
			$btnToggleUa.toggleClass("active", Omnisearch.isShowUa);
			if (isInitialHooks) return;
			this._doSearch();
		};
		Omnisearch.addHookUa(hkUa)
		hkUa();

		const $btnToggleBlacklisted = $(`<button class="btn btn-default" title="篩選黑名單中的內容結果">包含黑名單內容</button>`)
			.click(() => Omnisearch.doToggleBlacklisted());
		const hkBlacklisted = () => {
			$btnToggleBlacklisted.toggleClass("active", Omnisearch.isShowBlacklisted);
			if (isInitialHooks) return;
			this._doSearch();
		};
		Omnisearch.addHookBlacklisted(hkBlacklisted)
		hkBlacklisted();

		const handleMassExpandCollapse = mode => {
			SearchPage._isAllExpanded = mode;
			StorageUtil.pSetForPage("isExpanded", SearchPage._isAllExpanded);

			if (!SearchPage._rowMetas) return;
			SearchPage._rowMetas
				.filter(meta => meta.setIsExpanded)
				.forEach(meta => meta.setIsExpanded(mode));
		};

		const $btnCollapseAll = $(`<button class="btn btn-default" title="摺疊所有結果"><span class="glyphicon glyphicon-minus"></span></button>`)
			.click(() => handleMassExpandCollapse(false));

		const $btnExpandAll = $(`<button class="btn btn-default" title="展開所有結果"><span class="glyphicon glyphicon-plus"></span></button>`)
			.click(() => handleMassExpandCollapse(true));

		SearchPage._$wrpResults = $(`<div class="flex-col w-100">${this._getWrpResult_message("載入中...")}</div>`);

		$$(SearchPage._$wrp)`<div class="flex-col w-100 pg-search__wrp">
			<div class="flex-v-center mb-2 mobile__flex-col">
				<div class="flex-v-center input-group btn-group mr-2 w-100 mobile__mb-2">${$iptSearch}${$btnSearch}</div>

				<div class="flex-v-center">
					${$btnHelp}
					<div class="flex-v-center btn-group mr-2">
						${$btnToggleUa}
						${$btnToggleBlacklisted}
					</div>
					<div class="btn-group flex-v-center">
						${$btnCollapseAll}
						${$btnExpandAll}
					</div>
				</div>
			</div>
			${SearchPage._$wrpResults}
		</div>`;

		isInitialHooks = false;

		this._doSearch();
	}

	static _doSearch () {
		if (SearchPage._observer) {
			for (const ele of SearchPage._observed.keys()) SearchPage._observer.unobserve(ele);
		} else {
			SearchPage._observer = new IntersectionObserver(
				(obsEntries) => {
					obsEntries.forEach(entry => {
						if (entry.intersectionRatio > 0) { // filter observed entries for those that intersect
							SearchPage._observer.unobserve(entry.target);
							const meta = SearchPage._observed.get(entry.target);
							meta.onObserve();
						}
					});
				},
				{rootMargin: "150px 0px", threshold: 0.01},
			)
		}
		SearchPage._rowMetas = [];

		if (!location.search.slice(1)) {
			SearchPage._$wrpResults.empty().append(this._getWrpResult_message("輸入搜索內容來檢視結果"));
			return;
		}

		Omnisearch.pGetResults(decodeURIComponent(location.search.slice(1).replace(/\+/g, " ")))
			.then(results => {
				SearchPage._$wrpResults.empty();

				if (!results.length) {
					SearchPage._$wrpResults.append(this._getWrpResult_message("沒有找到結果。"));
					return;
				}

				SearchPage._rowMetas = results.map(result => {
					const r = result.doc;

					const $link = Omnisearch.$getResultLink(r);

					const {s: source, p: page, h: isHoverable, c: category, u: hash} = r;
					const ptPageInner = page ? `頁碼 ${page}` : "";
					const adventureBookSourceHref = SourceUtil.getAdventureBookSourceHref(source, page);
					const ptPage = ptPageInner && adventureBookSourceHref
						? `<a href="${adventureBookSourceHref}">${ptPageInner}</a>`
						: ptPageInner;

					const ptSourceInner = source ? `<i>${Parser.sourceJsonToFull(source)}</i> (<span class="${Parser.sourceJsonToColor(source)}" ${BrewUtil.sourceJsonToStyle(source)}>${Parser.sourceJsonToAbv(source)}</span>)` : `<span></span>`;
					const ptSource = ptPage || !adventureBookSourceHref
						? ptSourceInner
						: `<a href="${adventureBookSourceHref}">${ptSourceInner}</a>`;

					const $dispImage = $(`<div class="flex-col pg-search__disp-token mr-3 no-shrink"></div>`);
					const $dispPreview = $(`<div class="flex-col mobile__w-100"></div>`);
					const $wrpPreviewControls = $(`<div class="flex-col mobile__mb-2 mobile__w-100 h-100"></div>`);

					const out = {};

					const $row = $$`<div class="my-2 py-2 pl-3 pr-2 pg-search__wrp-result flex relative mobile__flex-col">
						<div class="flex-v-center mobile__mb-2 w-100">
							${$dispImage}
							<div class="flex-col flex-h-center mr-auto">
								<div class="mb-2">${$link}</div>
								<div>${ptSource}${ptPage ? `, ${ptPage}` : ""}</div>
							</div>
						</div>
						<div class="flex-v-center mobile__flex-col-reverse mobile__flex-ai-start">
							${$dispPreview}
							${$wrpPreviewControls}
						</div>
					</div>`.appendTo(SearchPage._$wrpResults);

					if (isHoverable) {
						out.isExpanded = !!SearchPage._isAllExpanded;

						const handleIsExpanded = () => {
							$dispPreview.toggleVe(out.isExpanded);
							$btnTogglePreview
								.html(out.isExpanded ? `<span class="glyphicon glyphicon-minus"></span>` : `<span class="glyphicon glyphicon-plus"></span>`)
								.toggleClass("pg-search__btn-toggle-preview--expanded", out.isExpanded);
						};

						out.setIsExpanded = val => {
							out.isExpanded = !!val;
							handleIsExpanded();
						};

						const observationTarget = $row[0];
						SearchPage._observed.set(
							observationTarget,
							{
								onObserve: () => {
									const page = UrlUtil.categoryToHoverPage(category);
									Renderer.hover.pCacheAndGet(
										page,
										source,
										hash,
									).then(ent => {
										// region Render tokens, where available
										let isImagePopulated = false;
										if (category === Parser.CAT_ID_CREATURE) {
											const hasToken = (ent.tokenUrl && ent.uniqueId) || ent.hasToken;
											if (hasToken) {
												isImagePopulated = true;
												const tokenUrl = Renderer.monster.getTokenUrl(ent);
												$dispImage.html(`<img src="${tokenUrl}" class="w-100 h-100">`);
											}
										}

										if (!isImagePopulated) $dispImage.addClass(`mobile__hidden`);
										// endregion

										// region Render preview
										Renderer.hover.$getHoverContent_stats(page, ent)
											.addClass("pg-search__wrp-preview mobile__w-100")
											.appendTo($dispPreview);
										// endregion
									});
								},
							},
						);
						SearchPage._observer.observe(observationTarget);

						const $btnTogglePreview = $(`<button class="btn btn-default btn-xs h-100" title="切換預覽"></button>`)
							.click(() => {
								out.isExpanded = !out.isExpanded;
								handleIsExpanded();
							})
							.appendTo($wrpPreviewControls);

						handleIsExpanded();
					}

					return out;
				});
			});
	}

	static _getWrpResult_message (message) {
		return `<div class="my-2 py-2 px-3 pg-search__wrp-result flex-vh-center"><i>${message.qq()}</i></div>`
	}
}
SearchPage._STORAGE_KEY_IS_EXPANDED = "isExpanded";
SearchPage._$wrp = null;
SearchPage._$wrpResults = null;
SearchPage._rowMetas = null;
SearchPage._observer = null;
SearchPage._observed = new Map();
SearchPage._isAllExpanded = false;

window.addEventListener("load", () => SearchPage.pInit());
