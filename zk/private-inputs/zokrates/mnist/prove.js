const fs = require('fs/promises');
const process = require('process');

const { initialize } = require('zokrates-js')


async function run() {
    let source = '';
    let sourceModelParams = '';
    let privInput = null;
    let pk = null;
    try {
        source = await fs.readFile('circuits/root.zok', { encoding: 'utf8' });
        sourceModelParams = await fs.readFile('circuits/model_params.zok', { encoding: 'utf8' });
        privInput = await fs.readFile('data/witness.json', { encoding: 'utf8' });
        privInput = JSON.parse(privInput);
        pk = await fs.readFile('data/pk.json', { encoding: 'utf8' });
        pk = JSON.parse(pk);
    } catch (err) {
        console.log(err);
        process.exit(1);
    }
        
    initialize().then((zokratesProvider) => {
        // compile
        const optionsCompile = { 
            config: { debug: true },
            location: "circuits/root.zok",
            //resolveCallback: fileSystemResolver
        };

        // TODO: Can't get resolveCallback to work, so for now we only replace 
        //       the model params import line with the actual source code.
        source = source.replace('from "./model_params" import WEIGHTS_0, WEIGHTS_1, BIASES_0, BIASES_1;', sourceModelParams);
        const artifacts = zokratesProvider.compile(source, optionsCompile);

        //computation
        let inputs = [
            privInput['inputs']
        ];
        
        let logs = [];
        const optionsExecute = {
            logCallback: (l) => {
               logs.push(l);
            },
        };
        const { witness, output } = zokratesProvider.computeWitness(artifacts, inputs, optionsExecute);
        console.log(logs);
        
        // generate proof
        const proof = zokratesProvider.generateProof(artifacts.program, witness, pk);
        fs.writeFile('data/proof.json', JSON.stringify(proof));
        
    });
}


run();

