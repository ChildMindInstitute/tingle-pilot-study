var synaptic = require('synaptic');

module.exports = {
  /**
   * @function train_lstm - Creates and trains a neural network
   * @param {int[]} nodes - number of nodes per layer
   * @param {Object} training_data - data on which to train the neural network
   * @param {Numeric[]} training_data.input - input values,
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
   * @param {Object} testingData - Object with string keys that indicate targets
   * @param {Numeric[][]} testingData[target].true - Array of numeric arrays of scaled ontarget input data
   * @param {Numeric[][]} testingData[target].false - Array of numeric arrays of scaled offtarget input data
   * @param {Object} network - Object with string keys that indicate targets. Must include at least all targets in testingData.
   * @param {LSTM} network[target] - LSTM trained to classify target as 1 and offtarget as 0
   * @returns {testOutputs}
   */
  test_lstms: function (testingData, network){
    /**
     * @typedef {Object} testOutputs - Object of outputs from trained LSTMs and input data
     * @property {Object} testOutputs[target] 
     */
    var testOutputs = {};
    for (var target in testingData) {
      testOutputs[target] = {"true":[],"false":[]};
      for(var iteration=0; iteration < testingData[target]["test_true"].length; iteration++){
        testOutputs[target]["true"].push(networks[target].activate(testingData[target]["test_true"][iteration]));
      }
      for(var iteration=0; iteration < testingData[target]["test_false"].length; iteration++){
        testOutputs[target]["false"].push(networks[target].activate(testingData[target]["test_false"][iteration]));
      }
    }
    return(testOutputs);
  }
};