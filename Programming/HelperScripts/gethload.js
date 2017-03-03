/*
 *  Javascript files can be loaded into the interactive console with:
 *      loadScript("/home/mattie432/Programming/Blockchain-Voting-System/Programming/HelperScripts/gethload.js")
 *  
 *  You can then call the functions defined below from the console.
 */

Custom = {
    
    checkAllBalances: function() {
        var totalBal = 0;
        for (var acctNum in eth.accounts) {
            var acct = eth.accounts[acctNum];
            var acctBal = web3.fromWei(eth.getBalance(acct), "ether");
            totalBal += parseFloat(acctBal);
            console.log("  eth.accounts[" + acctNum + "]: \t" + acct + " \tbalance: " + acctBal + " ether");
        }
        console.log("  Total balance: " + totalBal + " ether");
    },
    
    syncProgress: function() {
        var s = eth.syncing;
        console.log(
            "\n------------ GETH SYNCING PROGRESS\nprogress: " +
            (s.currentBlock/s.highestBlock*100) +
            " %\nblocks left to parse: " +
            (s.highestBlock-s.currentBlock) +
            "\ncurrent Block: " +
            s.currentBlock + " of " + s.highestBlock
        );
    },
    
    syncProgressFull : function() {
        /**
        *   GETH SYNCING PROGRESS - TIME ESTIMATE
        *  a script to estimate how much time is left to fully sync the Ethereum Blockchain with Geth
        *  
        *  If it takes too long, consider restarting geth with 
        *       the '--fast' option (not suggested for developers), 
        *       or better the '--cache=1024' or '--cache=2048 option that will assign more RAM to geth and make it faster
        * 
        *  (c) Lyricalpolymath 2016. MIT Licence 
        *  http://github.com/lyricalpolymath
        */
        
        
        // run like this
        // $ geth --exec "loadScript('GethSyncingProgress_2TimeEstimate.js')" attach  
        
                           
        //number of blocks to test before we give a timing estimate 
        var resolution = 10; 
        
        var startDate = new Date();
        var endDate;
        var s = eth.syncing;
        var block1 = s.currentBlock
        var blockLast = block1 + resolution
         
        
        // convert the duration for the stats
        function msToTime(duration) {
            var milliseconds = parseInt((duration % 1000) / 100),
                seconds = parseInt((duration / 1000) % 60),
                minutes = parseInt((duration / (1000 * 60)) % 60),
                hours = parseInt((duration / (1000 * 60 * 60)) % 24), 
                days = parseInt((duration / (1000 * 60 * 60 * 24)) % 365);
               
            var h = (hours < 10) ? "0" + hours : hours;
            var m = (minutes < 10) ? "0" + minutes : minutes;
            var s = (seconds < 10) ? "0" + seconds : seconds;
        
            return days + "d :" + hours + "h :" + minutes + "m :" + seconds + "s." + milliseconds;
        }
            
        
        function displayTimeEstimate() {
            s = eth.syncing;
            var blocksLeft = (s.highestBlock-s.currentBlock)   
            var time_duration = endDate - startDate  //returns amount of milliseconds passed
            var time_duration_readable = msToTime(time_duration);
            var time_left = msToTime( (time_duration / resolution) * blocksLeft );
            
            console.log("------------ GETH SYNCING PROGRESS - Time estimate")
            console.log("progress: " + (s.currentBlock/s.highestBlock*100));
            console.log("Estimated Time left*: " + time_left);
            console.log("Time it took to parse " + resolution + " blocks: " + time_duration_readable); 
            console.log("blocks left to parse: " + blocksLeft ); 
             
            if(time_duration_readable.indexOf("0d") != -1) {
                console.log("--------------------------------------------------") 
                console.log("*WARNING: this is just an ESTIMATE based on how much time it took to parse " + resolution + " blocks. But each block is different, some take longer than others because they have more transactions, and also, new blocks are continuously added");
                console.log("If it takes too long, consider restarting geth with the '--fast' option (not suggested for developers), or better the '--cache=1024' or '--cache=2048 option that will assign more RAM to geth and make it faster");
            }  
        }
        
        
        // wait untill the number of Blocks isn't like the BlockLast
        // and then calculate the time difference and show it on the console 
        console.log("\nGeth Syncing progress Time Estimate - STARTED - be patient, this might take ≈" + (resolution*5) + " seconds approximately")
        do {
           var cb = eth.syncing.currentBlock;
           if (cb >= blockLast) {
               endDate = new Date();
               displayTimeEstimate()
           }
        } while(cb < blockLast) 
        
    },
};
