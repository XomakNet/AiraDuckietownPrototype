var RobotLiabilityFactory = artifacts.require("./RobotLiabilityFactory.sol");

module.exports = function(deployer) {
  deployer.deploy(RobotLiabilityFactory);
};
