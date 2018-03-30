var assert = require('assert');
var synaptic = require('synaptic');
var lstm = require('../lstm.js');
var request = require('request');
var network = '';
var train = [];
var test_true = [];
var test_false = [];
var true_positive = [],
  true_negative = [];

function sum(total, num){
  return(total + num);
}

describe('lstm', function() {
  it('sample data loaded', function() {
    request({'uri': 'https://drive.google.com/uc?export=download&id=1IZmznJj9xr3DVRmJBe-BwncvDgdMvBIo', 'json': true}, function (error, response, demo_data) {
      var first = demo_data[0].true[0][0];
      assert.equal(first, 84.3);
    });
  });
  it('demo data formatted', function() {
    request({'uri': 'https://drive.google.com/uc?export=download&id=1IZmznJj9xr3DVRmJBe-BwncvDgdMvBIo', 'json': true}, function (error, response, demo_data) {
      var train = [];
      var test_true = [];
      var test_false = [];
      for (var t=0; t < 40; t++){
        train.push(
          {
            'input': demo_data[0].true[t].slice(0,5),
            'output': 1
          },
          {
            'input': demo_data[0].false[t].slice(0,5),
            'output': 0
          }
        );
        t2 = 40 + t;
        if (t2 < demo_data[0].true.length){
          test_true.push(
            demo_data[0].true[t2].slice(0,5)
          );
          test_false.push(
            demo_data[0].false[t2].slice(0,5)
          ); 
        }
      };
    });
  });
  it('test network training', function() {
    request({'uri': 'https://drive.google.com/uc?export=download&id=1IZmznJj9xr3DVRmJBe-BwncvDgdMvBIo', 'json': true}, function (error, response, demo_data) {
      for (var t=0; t < 40; t++){
        train.push(
          {
            'input': demo_data[0].true[t].slice(0,5),
            'output': [1]
          },
          {
            'input': demo_data[0].false[t].slice(0,5),
            'output': [0]
          }
        );
        t2 = 40 + t;
        if (t2 < demo_data[0].true.length){
          test_true.push(
            demo_data[0].true[t2].slice(0,5)
          );
          test_false.push(
            demo_data[0].false[t2].slice(0,5)
          ); 
        }
      };
      var Neuron = synaptic.Neuron,
        Layer = synaptic.Layer,
        Network = synaptic.Network,
        Trainer = synaptic.Trainer,
        Architect = synaptic.Architect;
      var LSTM = new Architect.LSTM(5,2,2,1);
      var trainer = new synaptic.Trainer(LSTM);
      network = trainer.train(
        train,
        {
          rate: 0.06,
          iterations: 100,
          error: 0.06,
          shuffle: false,
          log: 5,
          cost: Trainer.cost.CROSS_ENTROPY
        }
      );
      assert.isAbove(network.iterations, 2);
    });
  });
  it('true posititives', function() {
    request({'uri': 'https://drive.google.com/uc?export=download&id=1IZmznJj9xr3DVRmJBe-BwncvDgdMvBIo', 'json': true}, function (error, response, demo_data) {
      for (var t=0; t < 40; t++){
        train.push(
          {
            'input': demo_data[0].true[t].slice(0,5),
            'output': [1]
          },
          {
            'input': demo_data[0].false[t].slice(0,5),
            'output': [0]
          }
        );
        t2 = 40 + t;
        if (t2 < demo_data[0].true.length){
          test_true.push(
            demo_data[0].true[t2].slice(0,5)
          );
          test_false.push(
            demo_data[0].false[t2].slice(0,5)
          ); 
        }
      };
      LSTM_network = lstm.train_lstm(
        [5,2,2,1],
        train,
        0.06,
        0.06,
        100
      );
      for (t=0; t < test_true.length; t++) {
        true_positive.push(LSTM_network.activate(test_true[t]));
      };
      assert.equals(
        Math.round((true_positive.reduce(sum)/true_positive.length)),
        1
      );
    });   
  });
  it('true negatives', function() {
    request({'uri': 'https://drive.google.com/uc?export=download&id=1IZmznJj9xr3DVRmJBe-BwncvDgdMvBIo', 'json': true}, function (error, response, demo_data) {
      for (var t=0; t < 40; t++){
        train.push(
          {
            'input': demo_data[0].true[t].slice(0,5),
            'output': [1]
          },
          {
            'input': demo_data[0].false[t].slice(0,5),
            'output': [0]
          }
        );
        t2 = 40 + t;
        if (t2 < demo_data[0].true.length){
          test_true.push(
            demo_data[0].true[t2].slice(0,5)
          );
          test_false.push(
            demo_data[0].false[t2].slice(0,5)
          ); 
        }
      };
      LSTM_network = lstm.train_lstm(
        [5,2,2,1],
        train,
        0.06,
        0.06,
        100
      );
      for (t=0; t < test_true.length; t++) {
        true_positive.push(LSTM_network.activate(test_true[t]));
      };
      assert.equals(
        Math.round((true_positive.reduce(sum)/true_positive.length)),
        0
      );
    });   
  });
});