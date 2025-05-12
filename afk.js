const mineflayer = require('mineflayer');

const servers = [
    { host: 'sigmaboy9999.aternos.me', port: 28334, username: 'Bot1', version: '1.20.1' },
];

function createBot(server) {
    const bot = mineflayer.createBot({
        host: server.host,
        port: server.port,
        username: server.username,
        version: server.version, // Custom version
        auth: 'offline'
    });

    bot.on('spawn', () => {
        console.log(`${server.username} joined ${server.host}`);
        bot.chat(""); // Send message on join
        
    });

    bot.on('chat', (username, message) => {
        if (username !== bot.username) {
            bot.chat(`Hello ${username}, you said: ${message}`);
        }
    });

    bot.on('kicked', (reason) => {
        console.log(`${server.username} was kicked: ${reason}`);
        setTimeout(() => createBot(server), 5000); // Reconnect after 5 seconds
    });

    bot.on('end', () => {
        console.log(`${server.username} disconnected. Reconnecting...`);
        setTimeout(() => createBot(server), 5000);
    });

    bot.on('error', err => console.log(`Error: ${err}`));
}

// Start multiple bots
servers.forEach(createBot);