pragma solidity ^0.4.9;


import './dao/RobotLiability.sol';


contract RobotLiabilityFactory {

    event LiabilityRegistered(address liability, address promisor);

    function RobotLiabilityFactory() {}

    function createLiability(bytes _validation_model, uint256 _confirmation_count, address _promisee, address _promisor) public {
        RobotLiability liability = new RobotLiability(_validation_model, _confirmation_count, _promisee, _promisor);
        LiabilityRegistered(liability, _promisor);
    }
}