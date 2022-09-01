Types of usecases:

1) Run model on-chain:
    * Encode the whole trained model in script.
    * Results can be used arbitrarily in smart contracts.

2) Prove knowledge of input data:
    * Model encoded in circuit for zk-SNARK.
    * Prove the knowledge of a certain input that for which the trained model produces a specific output.
    * Only proof verifier is on-chain.

3) Prove possesion of trained model / pay someone for model training:
    * Structure of model is defined in circuit.
    * Weights and biases of the trained model are passed into the circuit as a private input.
    * Only proof verifier is on-chain.
