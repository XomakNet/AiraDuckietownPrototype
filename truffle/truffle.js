module.exports = {
    networks: {
        development: {
            host: "localhost",
            port: 8535,
            network_id: "1" // Match any network id
        },
        live: {
            host: "localhost",
            port: 8545,
            network_id: "*",
            gas: 4600000,
            from: "0xCF935e675e4E4C34320FDB804F362E2C572E5d7d"
        }
    }
};
