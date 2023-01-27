# Heimdall
A Cardano Node API and Notification Service

In Norse mythology, Heimdall (from Old Norse Heimdallr) is a god who keeps watch for invaders and the onset of Ragnarök from his dwelling Himinbjörg, where the burning rainbow bridge Bifröst meets the sky

Heimdall is a collection of 3 scripts - An API which receives client timestamp and block data, a client which uses a simple cardano-cli tip query to identify the clients latest synced block, and the watcher Heimdall who notifies the clients via email of any stagnant blocks/data

The API and client are designed to maintain anonymity - a 32bit token is created through an initialisation sequence through two curl requests. It is recommended you create a proton mail or skiff mail account to receive your notifications - although not scrictly necessary as Heimdall has no interest in your email address. If your timestamp is not updated for X time-period or your latest block is more than X blocks behind the actual cardano network tip a notification will be sent to the email associated with your token in your client API post request. 
