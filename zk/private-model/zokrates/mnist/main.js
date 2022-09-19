const fs = require('fs/promises');
const process = require('process');

const { initialize } = require('zokrates-js')


async function run() {
    let source = '';
    let modelData = null;
    let testData = null;
    try {
        source = await fs.readFile('circuits/root.zok', { encoding: 'utf8' });
        let modelDataStr = await fs.readFile('train/res.json', { encoding: 'utf8' });
        let testDataStr = await fs.readFile('train/test_examples.json', { encoding: 'utf8' });
        modelData = JSON.parse(modelDataStr);
        testData = JSON.parse(testDataStr);
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
        let privInputs = [
            modelData['weights'][0],
            modelData['weights'][1],
            modelData['biases'][0],
            modelData['biases'][1],
            testData['examples'],
            testData['labels']
        ];

        let logs = [];
        const optionsExecute = {
              logCallback: (l) => {
                logs.push(l);
              },
            };
        const { witness, output } = zokratesProvider.computeWitness(artifacts, privInputs, optionsExecute);
        console.log(logs);
    
        //// run setup
        //const keypair = zokratesProvider.setup(artifacts.program);
    
        //// generate proof
        //const proof = zokratesProvider.generateProof(artifacts.program, witness, keypair.pk);
    
        //// export solidity verifier
        //const verifier = zokratesProvider.exportSolidityVerifier(keypair.vk);
        //
        //// or verify off-chain
        //const isVerified = zokratesProvider.verify(keypair.vk, proof);
    });
}


run();

