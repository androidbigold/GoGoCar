// Import the page's CSS. Webpack will know what to do with it.
import "../stylesheets/app.css";

// Import libraries we need.
import { default as Web3} from 'web3';
import { default as contract } from 'truffle-contract'

// Import our contract artifacts and turn them into usable abstractions.
import cartoken_artifacts from '../../build/contracts/CarToken.json'
import carorder_artifacts from '../../build/contracts/CarOrder.json'

// CarToken is our usable abstraction, which we'll use through the code below.
var CarToken = contract(cartoken_artifacts);
var CarOrder = contract(carorder_artifacts);

// The following code is simple to show off interacting with your contracts.
// As your needs grow you will likely need to change its form and structure.
// For application bootstrapping, check out window.addEventListener below.
var accounts;
var account;

window.App = {
  start: function() {
    var self = this;

    // Bootstrap the CarToken abstraction for Use.
    CarToken.setProvider(web3.currentProvider);
    CarOrder.setProvider(web3.currentProvider);

    // Get the initial account balance so it can be displayed.
    web3.eth.getAccounts(function(err, accs) {
      if (err != null) {
        alert("There was an error fetching your accounts.");
        return;
      }

      if (accs.length == 0) {
        alert("Couldn't get any accounts! Make sure your Ethereum client is configured correctly.");
        return;
      }

      accounts = accs;
      account = accounts[0];
      self.refreshBalance();
    });
    var url = location.search;
    if(url.indexOf("?") != -1){
        var str = url.substr(1);
        var strs = str.split("&");
        document.getElementById("start").value = (strs[0].split("="))[1];
        document.getElementById("destination").value = (strs[1].split("="))[1];
        document.getElementById("amount").value = (strs[2].split("="))[1];
    }
  },

  setStatus: function(message) {
    var status = document.getElementById("status");
    status.innerHTML = message;
  },

  refreshBalance: function() {
    var self = this;

    var meta;
    CarToken.deployed().then(function(instance) {
      meta = instance;
      return meta.balanceOf(account, {from: account});
    }).then(function(value) {
      var balance_element = document.getElementById("balance");
      balance_element.innerHTML = value.valueOf();
    }).catch(function(e) {
      console.log(e);
      self.setStatus("Error getting balance; see log.");
    });
  },

  sendCoin: function() {
    var self = this;

    this.setStatus("Initiating transaction... (please wait)");

    var recipient = document.getElementById("recipient").value;
    var start = document.getElementById("start").value;
    var destination = document.getElementById("destination").value;
    var amount = parseInt(document.getElementById("amount").value);
    var score = parseInt(document.getElementById("score").value);

    var meta;
    CarToken.deployed().then(function(instance) {
      meta = instance;
      return meta.transfer(recipient, amount, {from: account, gas: 4712388, gasPrice: 100000000000});
    }).then(function(status) {
      self.setStatus("Transfer successed!");
      self.pushOrder(recipient, start, destination, amount, score);
      self.refreshBalance();
    }).catch(function(e) {
      console.log(e);
      self.setStatus("Error sending coin; see log.");
    });
  },

  pushOrder: function(recipient, start, destination, amount, score) {
    var self = this;
    var meta;
    var nowtime = new Date().getTime();

    CarOrder.deployed().then(function(instance) {
      meta = instance;
      return meta.PushOrder(start, destination, amount, score, String(nowtime), recipient, {from: account});
    }).then(function(status) {
      	return meta.getOrderIndex.call(start, destination, amount, score, String(nowtime), recipient, {from: account});
    }).then(function(index) {
    	self.setStatus("Order pushed! Order index is: " + String(index));
    }).catch(function(e) {
        self.setStatus("Error pushing order; see log.");
    });
  },

  searchOrder: function() {
    var self = this;
    var meta;

    var index = prompt("Please input the index of order you want to search.");
    CarOrder.deployed().then(function(instance) {
      meta = instance;
      return meta.orderList.call(index);
    }).then(function(order) {
      alert("sender: " + order[0]
          + "\nrecipient: " + order[1]
          + "\nstart: " + order[2]
          + "\ndestination: " + order[3]
          + "\namount: " + order[4]
          + "\nscore: " + order[5]
          + "\ntimestamp: " + order[6]);
    }).catch(function(e) {
      alert("Search failed!");
    });
  },

  searchOrderFromList: function(index) {
    var self = this;
    var meta;

    CarOrder.deployed().then(function(instance) {
      meta = instance;
      return meta.orderList.call(index);
    }).then(function(order) {
      alert("sender: " + order[0]
          + "\nrecipient: " + order[1]
          + "\nstart: " + order[2]
          + "\ndestination: " + order[3]
          + "\namount: " + order[4]
          + "\nscore: " + order[5]
          + "\ntimestamp: " + order[6]);
    }).catch(function(e) {
      alert("Get order information failed!");
    });
  },

  importAccount: function() {
  	var self = this;

  	var pk = document.getElementById("private_key").value;
  	var pw = document.getElementById("password").value;

  	web3.personal.importRawKey(pk, pw, function(err, acc) {
  		if (err != null)
  			self.setStatus(err);
  		else
  			alert(String(acc) + " has been imported");
  	});
  },

  getOrder: function(count) {
    var self = this;
    var meta;

    CarOrder.deployed().then(function(instance) {
        meta = instance;
        return meta.personalorderList.call(account, count);
    }).then(function(orderIndex) {
        try{
            var isOrder = typeof orderIndex;
            if(isOrder == "string"){
                var node = document.createElement("li");
                node.setAttribute("id", "order");
                node.innerHTML = String(orderIndex);
                node.onclick = function(){
                    self.searchOrderFromList(this.innerHTML);
                };

                var ul = document.getElementById("list");
                ul.appendChild(node);
                self.getOrder(count + 1);
            }
        }
        catch(e){
            alert("Search history orders failed!");
        }
    }).catch(function(e) {
        alert("All history orders are found!");
    });
  },

  getOrderList: function() {
    var self = this;

    self.getOrder(0);
  },

  getScore: function() {
    var self = this;
    var meta;

    var address = document.getElementById("address").value;

    CarOrder.deployed().then(function(instance) {
       meta = instance;
       return meta.scoreList.call(address);
    }).then(function(Score) {
       alert("Score: " + Score[0]
             + "\nRatings: " + Score[1]);
    }).catch(function(e) {
       alert("Search failed!" + e);
    });
  },

  findBestDriver: function() {
    var self = this;
    var meta;
    var best_pop = 0;
    var best_driver;

    web3.eth.getAccounts(function(err, accs) {
      if (err != null) {
        console.log("There was an error fetching your accounts.");
        return;
      }

      if (accs.length == 0) {
        console.log("Couldn't get any accounts! Make sure your Ethereum client is configured correctly.");
        return;
      }

      accounts = accs;
    });

    CarOrder.deployed().then(function(instance) {
        meta = instance;
        for(var i = 1; i < accounts.length; i++){
            meta.scoreList.call(accounts[i]).then(function(Score) {
                if(Score[1] > best_pop){
                    best_pop = Score[1];
                    best_driver = accounts[i];
                }
                meta.clearScore.call(accounts[i], {from: accounts[0]});
            });
        }
        return best_driver;
    }).catch(function(e) {
        console.log("findBestDriver failed! " + e);
    });

  },

  reward: function() {
    var self = this;
    var meta;

    CarToken.deployed().then(function(instance) {
        meta = instance;
        return self.findBestDriver();
    }).then(function(driver) {
        meta.Reward.call(driver, {from: accounts[0]});
    }).catch(function(e) {
        console.log("Reward failed! " + e);
    });
  }

};

window.addEventListener('load', function() {
  // Checking if Web3 has been injected by the browser (Mist/MetaMask)
  if (typeof web3 !== 'undefined') {
    console.warn("Using web3 detected from external source. If you find that your accounts don't appear or you have 0 CarToken, ensure you've configured that source properly. If using MetaMask, see the following link. Feel free to delete this warning. :) http://truffleframework.com/tutorials/truffle-and-metamask")
    // Use Mist/MetaMask's provider
    window.web3 = new Web3(web3.currentProvider);
  } else {
    console.warn("No web3 detected. Falling back to http://127.0.0.1:8545. You should remove this fallback when you deploy live, as it's inherently insecure. Consider switching to Metamask for development. More info here: http://truffleframework.com/tutorials/truffle-and-metamask");
    // fallback - use your fallback strategy (local node / hosted node + in-dapp id mgmt / fail)
    window.web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:8545"));
  }

  App.start();
});

window.setInterval(App.reward, 1000 * 600);
