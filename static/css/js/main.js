// MetaMask wallet connection logic
const connectButton = document.getElementById("connectButton");
const walletStatus = document.getElementById("walletStatus");

// Detect if MetaMask is installed
if (typeof window.ethereum !== 'undefined') {
    console.log('MetaMask is installed!');

    // Set up click event to connect wallet
    connectButton.onclick = async () => {
        try {
            // Request account access from MetaMask
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
            const account = accounts[0];

            // Update the UI
            walletStatus.innerText = `Connected wallet: ${account}`;
            console.log(`Connected wallet: ${account}`);
        } catch (error) {
            console.error('Error connecting to MetaMask:', error);
            walletStatus.innerText = "Error connecting wallet";
        }
    };
} else {
    walletStatus.innerText = "MetaMask not installed";
    console.log('MetaMask not detected.');
}
