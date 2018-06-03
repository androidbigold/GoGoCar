var CarToken = artifacts.require("./CarToken.sol");
var CarOrder = artifacts.require("./CarOrder.sol");


module.exports = function(deployer) {
  deployer.deploy(CarToken);
  deployer.deploy(CarOrder);
};
