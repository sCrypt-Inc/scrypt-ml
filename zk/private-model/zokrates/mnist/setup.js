const fs = require('fs/promises');
const process = require('process');

const { initialize } = require('zokrates-js')


async function run() {
    let source = '';
    try {
        source = await fs.readFile('circuits/root.zok', { encoding: 'utf8' });
    } catch (err) {
        console.log(err);
        process.exit(1);
    }
        
    initialize().then((zokratesProvider) => {
        // compilation
        const optionsCompile = { 
            config: { debug: true }
        };
        const artifacts = zokratesProvider.compile(source, optionsCompile);
    
        // run setup
        const keypair = zokratesProvider.setup(artifacts.program);
        fs.writeFile('data/vk.json', JSON.stringify(keypair.vk));
        fs.writeFile('data/pk.json', JSON.stringify(keypair.pk));
    });
}


run();

