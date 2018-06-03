pragma solidity ^0.4.17;


contract CarOrder{
    address public minter;
	struct Order{
		address sender;
		address recipient;
		string start;
		string destination;
		uint256 amount;
		uint256 score;
		string timestamp;
	}

	struct Score{
		uint256 score;
		uint256 number;
	}

	mapping(bytes32 => Order) public orderList;
	mapping(address => Score) public scoreList;
	mapping(address => bytes32[]) public personalorderList;

    constructor() public {
        minter = msg.sender;
    }

	function PushOrder(string _start, string _destination, uint256 _amount, uint256 _score, string _timestamp, address _recipient) public {
		bytes32 orderHash;
		orderHash = sha256(msg.sender, _recipient, _start, _destination, _amount, _score, _timestamp);
		orderList[orderHash] = Order(msg.sender, _recipient, _start, _destination, _amount, _score, _timestamp);
		scoreList[_recipient] = Score((scoreList[_recipient].score * scoreList[_recipient].number + _score) / (scoreList[_recipient].number + uint256(1)), (scoreList[_recipient].number + uint256(1)));
	    personalorderList[msg.sender].push(orderHash);
	    personalorderList[_recipient].push(orderHash);
	}

	function getOrderIndex(string _start, string _destination, uint256 _amount, uint256 _score, string _timestamp, address _recipient) public view returns (bytes32) {
		bytes32 OrderIndex;
		OrderIndex = sha256(msg.sender, _recipient, _start, _destination, _amount, _score, _timestamp);
		return OrderIndex;
	}

	function clearScore(address _recipient) public {
	    if(msg.sender != minter) return;
	    delete scoreList[_recipient];
	}

}