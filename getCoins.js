const axios = require('axios');
const fs = require('fs');

async function main() {
	const instance = axios.create({
		baseURL: "https://api.coingecko.com/api/v3",
	});

	let coinIds = [];
	const getIds = async (number) => {
		try {
			const response = await instance.get(
				`/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=${number}&sparkline=false`
			);
			coinIds = [...coinIds, ...response.data.map((coin) => coin.id)];
			console.log("🚀 ~ file: apiCall.js ~ line 14 ~ getIds ~ coinIds", coinIds);
		} catch (e) {
			console.log("🚀 ~ file: apiCall.js ~ line 17 ~ getIds ~ e", e.message);
		}
	};
	let id = [];
	for (let i = 1; i <= 10; i++) {
		idddd = await getIds(i);
	}
	id = coinIds;
	fs.writeFile('coins.txt', JSON.stringify(id), err => {
		if (err) {
			console.error(err);
		}
	})
}

main();