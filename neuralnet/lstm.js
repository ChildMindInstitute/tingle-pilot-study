var synaptic = require('synaptic');

module.exports = {
  /**
   * @function train_lstm - Creates and trains a neural network
   * @param {int[]} nodes - number of nodes per layer
   * @param {Object} training_data - data on which to train the neural network
   * @param {Numeric[]} training_data.input - input values
   * @param {Numeric[]} training_data.output - output values
   * same number as the first value in nodes
   * @param {Numeric} nnError - minimum error value
   * @param {Numeric} nnRate
   * @param {int} nnIterations - number of training rounds
   * @returns {LSTM}
   */
  train_lstm: function (nodes, training_data, nnError, nnRate, nnIterations) {
    var Neuron = synaptic.Neuron,
    Layer = synaptic.Layer,
    Network = synaptic.Network,
    Trainer = synaptic.Trainer,
    Architect = synaptic.Architect;
    var LSTM = new Architect.LSTM(...nodes);
    var trainer = new synaptic.Trainer(LSTM);

    console.log(
      "\nTRAINING 🏋 interations:" + nnIterations +
      " 🏋 minimum error:" + nnError +
      " 🏋 rate:" + nnRate
    );
    trainer.train(
      training_data, {
        rate: nnRate,
        iterations: nnIterations,
        error: nnError,
        shuffle: false,
        log: 5,
        cost: Trainer.cost.CROSS_ENTROPY
      });
    console.log("🏋 trained!");
    return(LSTM);
  },
  /**
   * @function test_lstms - Tests an Array of neural networks
   * @param {Object} testingData - data on which to train the neural network
   * @param {Numeric[]} testingData.input - input values
   * @param {Numeric[]} testingData.output - output values
   * @param {Object} network - Object with string keys that indicate targets. Must include at least all targets in testingData.
   * @returns {testOutputs}
   */
  test_lstms: function (testingData, network){
    /**
     * @typedef {Object} testOutputs - Object of outputs from trained LSTMs and input data
     * @property {Object} testOutputs[target] 
     */
    var testOutputs = {};
    for(var iteration=0; iteration < testingData.length; iteration++){
      if (!(testingData[iteration].output in testOutputs)) {
        testOutputs[testingData[iteration].output] = [];
      }
      testOutputs[testingData[iteration].output].push(network.activate(testingData[iteration].input));
    }
    return(testOutputs);
  }
};