// management/static/js/daily_entry_logic.js

document.addEventListener('DOMContentLoaded', function() {
    const canteenSelect = document.getElementById('id_canteen');
    const supplyRows = document.querySelectorAll('.field-lunch_qty, .field-dinner_qty, .field-nasta_qty, .field-tea_qty');
    const paymentRows = document.querySelectorAll('.field-cash_received, .field-online_received');
    const teaRow = document.querySelector('.field-tea_qty');

    // 1. सर्वर से कैंटीन का डेटा मंगाएं (Automatic!)
    // ध्यान दें: अगर आपका URL prefix अलग है, तो इसे '/management/get-canteen-data/' करें
    fetch('/management/get-canteen-data/') 
        .then(response => response.json())
        .then(CANTEEN_MAP => {
            console.log("Loaded Canteen Data:", CANTEEN_MAP); // कंसोल में चेक करें कि डेटा आया या नहीं

            function toggleFields() {
                const canteenId = canteenSelect.value;
                
                // Map से billing type निकालें (अब यह ऑटोमैटिक है)
                const billingType = CANTEEN_MAP[canteenId];

                // शुरू में सबको छिपाएं
                supplyRows.forEach(el => el.style.display = 'none');
                paymentRows.forEach(el => el.style.display = 'none');

                if (billingType) {
                    // Supply Fields हमेशा दिखाएं
                    supplyRows.forEach(el => el.style.display = '');

                    if (billingType === 'DAILY') {
                        paymentRows.forEach(el => el.style.display = ''); 
                        if(teaRow) teaRow.style.display = ''; 
                    } else if (billingType === 'MONTHLY') {
                        if(teaRow) teaRow.style.display = 'none';
                    }
                }
            }

            if (canteenSelect) {
                canteenSelect.addEventListener('change', toggleFields);
                toggleFields(); // पेज लोड होने पर चलाएं
            }
        })
        .catch(error => console.error('Error loading canteen data:', error));
});