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
        shuffle: true,
        log: 5,
        cost: Trainer.cost.CROSS_ENTROPY
      });
    console.log("🏋 trained!");
    return(LSTM);
  }
};