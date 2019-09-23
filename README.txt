"Hi I noticed that your cashier system is a bit slow so I hope that 
this software may speed it up for you" BR. Jacob

Each day the software generates two logs, a dated registry file and
a dated status file. 

Registry tracks history and status tracks current situation. 
Whenever a customer pays off debt a receipt file will generate in
the receipts folder.

The ordernum.json keeps track of the current order number count.
Open it and set the value to whatever ordernumber you are currently on, save.

The sign.json generates a prefix used locally depending on where it is used.
For instance one may be named "BeachBar" and another one "Lobby".
The prefix will precede any log generated. 

If the sign file is missing, one will be created upon starting the application.

The software will automatically add prices & debt for rooms, extended stays, food,
drinks & snacks. Just make sure to update the purchase.json if you change prices
or add more items. 

Registry tracks all purchases and debt generated, Status tracks the current debt.
Since one Status file generates per day, remember to take logs of past days into
account when calculating debt. STATUS FILE ONLY READS STATUS FOR CURRENT DAY! 

Some bugs may occur causing the software to crash, but in most cases is due to
invalid input. 
Please report all bugs you experience as thorough as possible.
