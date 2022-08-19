pragma solidity >=0.8.4<0.9.0;
contract Altcoin{
    // Introducing maximum number of Altcoins available for sale
    uint public max_Altcoin=100000;
    //Introducing USD to Altcoin convert rate
      uint public usd_Altcoin=1000;

    // Introducing total number of Altcoins that are brought by investers
    uint public total_Altcoins_brought=0;

    //mapping from the invester address to its equity in Altcoins in USD
    mapping(address=>uint)  equity_Alt;
    mapping(address=>uint) equity_USD;

    //checking on invester can buy a Altcoins
    modifier can_buy_Altcoin(uint usd_invested){
        require(usd_invested*usd_Altcoin+total_Altcoins_brought<=max_Altcoin);
        _;
    }
    //Getting Equity in Altcoins by Invester
    function equity_in_Altcoins(address invester) external  returns(uint){
        return equity_Alt[invester];
    }

    //Getting Equity in USD by Invester
      function equity_in_USD(address invester) external  returns(uint){
        return equity_USD[invester];
    }
    //Buy Altcoins
    function Buy_Altcoins(address invester,uint usd_invested) external
    can_buy_Altcoin(usd_invested){
        uint Altcoins_brought=usd_invested*usd_Altcoin;
        equity_Alt[invester]+=Altcoins_brought;
        equity_USD[invester]= equity_Alt[invester]/1000;
        total_Altcoins_brought+=Altcoins_brought;


    }
    //Selling Altcoins
    function Sell_Altcoins(address invester,uint Altcoin_sold) external{
        equity_Alt[invester]-=Altcoin_sold;
        equity_USD[invester]= equity_Alt[invester]/1000;
        total_Altcoins_brought-=Altcoin_sold;


    }

}
