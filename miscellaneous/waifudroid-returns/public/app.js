const vm = require(`vm`);
const Discord = require(`discord.js`);
const client = new Discord.Client();

const { secret } = require(`./secrets.js`);

const responses = {
    reticent: [`No.`, `Go away...`, `I don't want to talk to you..`, `Hmm.`, `I don't know.`, `\u{1F610}`, `\u{1F910}`, `Maybe not.`, `Bye.`],
    secret: secret
};

const sanitize = (str) =>
{
    if(/constructor/i.test(str))
    {
        str = str.replace(/constructor/i, ``);
    } else if(/justonemoresecret/i.test(str)) {
		str = str.replace(/justonemoresecret/i, ``);
	} else {
		return str;
	}
	return sanitize(str);
};

const fetchResponse = (responseType) =>
{
    return responses[responseType][Math.floor(Math.random() * responses[responseType].length)];
};

const lower = (str) => { return str.toLowerCase(); };

client.on(`message`, (msg) =>
{
    let user = msg.author;
    if(msg.channel.type != `dm` || user == client.user) return;
    let content = sanitize(msg.content.replace(/[0-9\\"'`+]/g, ``));

    try
    {
        content = lower(vm.runInNewContext(`${content}`));
    } catch(err) {
        content = ``;
    }
	
	if(content == `justonemoresecret`) 
	{
		user.send(fetchResponse(`secret`));
	} else {
		user.send(fetchResponse(`reticent`));
	}
});

client.login(process.env.BOT_TOKEN);
