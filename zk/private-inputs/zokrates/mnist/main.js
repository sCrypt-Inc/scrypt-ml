const fs = require('fs/promises');
const process = require('process');

const { initialize } = require('zokrates-js')


async function run() {
    let source = '';
    let witness = null;
    try {
        source = await fs.readFile('circuits/root.zok', { encoding: 'utf8' });
        let witness = await fs.readFile('data/witness.json', { encoding: 'utf8' });
        witness = JSON.parse(witness);
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
    
        // computation
        let inputs = [
            witness['inputs']
        ];

        let logs = [];
        const optionsExecute = {
              logCallback: (l) => {
                logs.push(l);
              },
            };
        const { witness, output } = zokratesProvider.computeWitness(artifacts, inputs, optionsExecute);
        console.log(logs);
    
        // run setup
        const keypair = zokratesProvider.setup(artifacts.program);
    
        // generate proof
        const proof = zokratesProvider.generateProof(artifacts.program, witness, keypair.pk);
    
        // export sCrypt verifier
        const verifier = zokratesProvider.exportScryptVerifier(keypair.vk);
        
    });
}


run();

