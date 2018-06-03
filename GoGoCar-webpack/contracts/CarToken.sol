pragma solidity ^0.4.17;
import "zeppelin-solidity/contracts/token/ERC20/StandardToken.sol";

contract CarToken is StandardToken {
  string public name = "CarCoin";
  string public symbol = "CC";
  uint8 public decimals = 0;
  uint256 public INITIAL_SUPPLY = 8888;
  uint256 public REWARD_TOKEN = 20;
  address public minter;

  constructor() public {
    totalSupply_ = INITIAL_SUPPLY;
    balances[msg.sender] = INITIAL_SUPPLY;
    minter = msg.sender;
  }

  function Reward(address recipient) public {
    if(msg.sender != minter) return;
    balances[recipient] += REWARD_TOKEN;
  }

}