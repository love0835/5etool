async function main () {
	require("./generate-dmscreen-reference");
	require("./generate-quick-reference");
	await require("./generate-tables-data");
	require("./generate-subclass-lookup");
	await require("./generate-search-index");
	// require("./generate-wotc-homebrew"); // unused
}

main().catch(e => { throw e; });
