// ==UserScript==
// @name         STV Claim (FormData POST) - Optimized
// @namespace    http://tampermonkey.net/
// @version      2025-06-02
// @description  Gửi POST request với FormData, nhận JSON và hiển thị toast nếu code === 1 cùng quản lý danh sách vật phẩm và reload tự động khi cần.
// @author       You
// @match        https://sangtacviet.app/truyen/*/1/*/*/
// @icon         https://www.google.com/s2/favicons?sz=64&domain=sangtacviet.app
// @grant        GM_xmlhttpRequest
// @connect      *
// ==/UserScript==

(function () {
    'use strict';

    /* =================== UTILITY FUNCTIONS =================== */

    // Lưu, lấy cài đặt từ localStorage
    const saveSetting = (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    };

    const getSetting = (key) => {
        const val = localStorage.getItem(key);
        return val ? JSON.parse(val) : null;
    };

    // Lưu vật phẩm đã nhặt vào localStorage (cập nhật timestamp và count nếu đã tồn tại)
    const saveItem = (name) => {
        const items = JSON.parse(localStorage.getItem("collectedItems")) || [];
        const timestamp = new Date().toLocaleString();
        const index = items.findIndex(item => item.name === name);
        if (index !== -1) {
            items[index].timestamp = timestamp;
            items[index].count = (items[index].count || 1) + 1;
        } else {
            items.push({ name, timestamp, count: 1 });
        }
        localStorage.setItem("collectedItems", JSON.stringify(items));
    };

    // Hiển thị thông báo dưới dạng toast (tự ẩn sau 3 giây)
    const showToast = (message) => {
        let toastContainer = document.getElementById('tm-toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'tm-toast-container';
            Object.assign(toastContainer.style, {
                position: 'fixed',
                bottom: '120px',
                left: '20px',
                zIndex: 9999
            });
            document.body.appendChild(toastContainer);
        }
        const toast = document.createElement('div');
        toast.innerText = message;
        Object.assign(toast.style, {
            background: '#28a745',
            color: '#fff',
            padding: '10px 15px',
            marginTop: '10px',
            borderRadius: '5px',
            boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
            opacity: '1',
            transition: 'opacity 0.5s ease'
        });
        toastContainer.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    };

    /* =================== UI BUTTONS =================== */

    // Tạo nút cài đặt (bật/tắt reload tự động)
    const createSettingButton = () => {
        const currentSetting = getSetting("autoReload");
        const settingBtn = document.createElement("button");
        settingBtn.id = "settingBtn";
        settingBtn.innerText = "⚙️ Reload: " + (currentSetting ? "BẬT" : "TẮT");
        Object.assign(settingBtn.style, {
            position: "fixed",
            bottom: "70px",
            left: "20px",
            padding: "10px",
            background: "#28a745",
            color: "#fff",
            border: "none",
            cursor: "pointer",
            borderRadius: "5px"
        });
        settingBtn.onclick = toggleAutoReload;
        document.body.appendChild(settingBtn);
    };

    const toggleAutoReload = () => {
        const currentSetting = getSetting("autoReload") || false;
        const newSetting = !currentSetting;
        saveSetting("autoReload", newSetting);
        const settingBtn = document.getElementById('settingBtn');
        if (settingBtn) {
            settingBtn.innerText = "⚙️ Reload: " + (newSetting ? "BẬT" : "TẮT");
        }
        showToast("Chế độ tự động reload khi lỗi nhặt được đồ: " + (newSetting ? "BẬT" : "TẮT"));
    };

    // Tạo nút hiển thị danh sách vật phẩm
    const createShowButton = () => {
        const showBtn = document.createElement("button");
        showBtn.innerText = "🗃 Vật phẩm";
        Object.assign(showBtn.style, {
            position: "fixed",
            bottom: "20px",
            left: "20px",
            padding: "10px",
            background: "#007bff",
            color: "#fff",
            border: "none",
            cursor: "pointer",
            borderRadius: "5px"
        });
        showBtn.onclick = showItemList;
        document.body.appendChild(showBtn);
    };

    // Hiển thị danh sách vật phẩm từ localStorage; nhóm, sắp xếp theo thời gian nhặt gần nhất
    function showItemList() {
        // Lấy dữ liệu từ localStorage và kiểm tra tính tồn tại của vật phẩm
        const rawData = localStorage.getItem("collectedItems");
        const items = rawData ? JSON.parse(rawData) : [];
        if (items.length === 0) {
            alert("Không có vật phẩm nào!");
            return;
        }

        // Nhóm các mục theo tên hoặc theo loại nếu có quy tắc:
        const grouped = items.reduce((acc, curr) => {
            let key = curr.name.includes("Linh Thạch") ? "Linh Thạch" :
            curr.name.includes("Tụ Khí Đan") ? "Tụ Khí Đan" :
            curr.name.includes("Tẩy Tủy Đan") ? "Tẩy Tủy Đan" :
            curr.name.includes("Tụ Linh Đan") ? "Tụ Linh Đan" :
            curr.name.includes("Thiên Vận Đan") ? "Thiên Vận Đan" :
            (curr.name.includes("Tàn quyển") || curr.name.includes("Thân pháp") || curr.name.includes("Công kích") || curr.name.includes("Phòng ngự") || curr.name.includes("Luyện thể") || curr.name.includes("Tinh thần")) ? "Vũ kỹ" :
            curr.name.includes("Pháp Tắc") ? "Pháp Tắc"
            : curr.name;

            if (!acc[key]) {
                acc[key] = {
                    count: curr.count || 1,
                    // Lưu thời gian nhặt ở dạng Date để dễ sắp xếp
                    lastTimestamp: new Date(curr.timestamp)
                };
            } else {
                acc[key].count += (curr.count || 1);
                let currTime = new Date(curr.timestamp);
                if (currTime > acc[key].lastTimestamp) {
                    acc[key].lastTimestamp = currTime;
                }
            }
            return acc;
        }, {});

        // Chuyển đổi đối tượng thành mảng và sắp xếp theo thời gian nhặt gần nhất (giảm dần)
        const sortedItems = Object.keys(grouped)
        .map(name => ({
            name,
            count: grouped[name].count,
            lastTimestamp: grouped[name].lastTimestamp
        }))
        .sort((a, b) => b.lastTimestamp - a.lastTimestamp);

        // Xóa container danh sách cũ nếu có
        let listDiv = document.getElementById("itemList");
        if (listDiv) listDiv.remove();

        // Tạo container danh sách mới sử dụng CSS Grid với 2 cột cố định
        listDiv = document.createElement("div");
        listDiv.id = "itemList";
        Object.assign(listDiv.style, {
            position: "fixed",
            bottom: "60px",
            left: "20px",
            background: "#fff",
            border: "1px solid #ddd",
            boxShadow: "0px 2px 6px rgba(0,0,0,0.2)",
            borderRadius: "5px",
            padding: "15px",
            width: "600px",
            maxHeight: "1000px",
            overflowY: "auto",
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)", // 2 cột cố định
            gap: "15px",
            zIndex: "10000"
        });
        document.body.appendChild(listDiv);

        // Thêm tiêu đề cho danh sách
        const title = document.createElement("div");
        title.innerHTML = "<strong>Danh sách vật phẩm:</strong>";
        title.style.gridColumn = "span 2"; // Tiêu đề kéo dài trên 2 cột
        listDiv.appendChild(title);

        // Hiển thị từng mục theo dạng 2 cột
        sortedItems.forEach((item, index) => {
            const itemDiv = document.createElement("div");
            Object.assign(itemDiv.style, {
                padding: "2px",
                background: "#f8f9fa",
                borderRadius: "5px",
                textAlign: "center",
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
            });
            itemDiv.innerHTML = `<strong>${item.name}</strong><br>(x${item.count})<br>Gần nhất: ${item.lastTimestamp.toLocaleString()}`;
            listDiv.appendChild(itemDiv);
        });

        // Nút "Xóa danh sách" hiện trên 2 cột
        const clearBtn = document.createElement("button");
        clearBtn.innerText = "🗑 Xóa danh sách";
        Object.assign(clearBtn.style, {
            gridColumn: "span 2",
            padding: "5px",
            background: "#dc3545",
            color: "#fff",
            border: "none",
            cursor: "pointer",
            borderRadius: "5px"
        });
        clearBtn.onclick = clearItemList;
        listDiv.appendChild(clearBtn);

        // Nút "Đóng danh sách" hiện trên 2 cột
        const closeBtn = document.createElement("button");
        closeBtn.innerText = "❌ Đóng";
        Object.assign(closeBtn.style, {
            gridColumn: "span 2",
            padding: "5px",
            background: "#6c757d",
            color: "#fff",
            border: "none",
            cursor: "pointer",
            borderRadius: "5px"
        });
        closeBtn.onclick = () => { listDiv.style.display = "none"; };
        listDiv.appendChild(closeBtn);
    }

    function clearItemList() {
        localStorage.removeItem("collectedItems");
        const listDiv = document.getElementById("itemList");
        if (listDiv) listDiv.remove();
        alert("Đã xóa danh sách vật phẩm!");
    }


    /* =================== NETWORK (GM_xmlhttpRequest) =================== */

    // Bọc GM_xmlhttpRequest trong Promise cho dễ dàng sử dụng async/await
    const sendFormData = (url, formData) => {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                method: "POST",
                url: url,
                data: formData,
                onload: (response) => {
                    try {
                        const json = JSON.parse(response.responseText);
                        resolve(json);
                    } catch (e) {
                        console.error("Lỗi khi phân tích JSON:", e);
                        reject(e);
                    }
                },
                onerror: (error) => {
                    console.error("Yêu cầu thất bại:", error);
                    reject(error);
                }
            });
        });
    };

    /* =================== MAIN LOGIC =================== */

    // Hàm poll server lấy thông tin vật phẩm theo chu kỳ
    const pollForItems = async () => {
        // Tạo request check
        const checkData = new FormData();
        checkData.append("ngmar", "tcollect");
        checkData.append("ajax", "trycollect");
        checkData.append("iscollectable", "iscollectable");
        const targetUrl = window.location.origin + "/index.php?ngmar=iscollectable";

        try {
            const check = await sendFormData(targetUrl, checkData);
            if (check.code && check.code === 1) {
                // Nếu có đồ, tiến hành lấy thông tin vật phẩm
                const url = window.location.origin + "/index.php";
                const itemData = new FormData();
                itemData.append("ngmar", "collect");
                itemData.append("ajax", "collect");

                // Chờ 1 giây để gọi request item (giả lập độ trễ)
                const item = await new Promise(resolve => setTimeout(() => {
                    sendFormData(url, itemData).then(resolve).catch(() => resolve(null));
                }, 1000));

                if (item && item.type) {
                    const claimData = new FormData();
                    const lastStr = window.location.href.replace(/\/$/, "").split("/").pop();
                    claimData.append("ajax", "fcollect");
                    claimData.append("c", lastStr);
                    if ([3, 4].includes(item.type)) {
                        claimData.append("newname", item.name ? item.name.replace(/<br>/g, '').replace(/<b>/g, '').replace(/<\/b>/g, '') : '');
                        claimData.append("newinfo", item.info ? item.info.replace(/<br>/g, '').replace(/<b>/g, '').replace(/<\/b>/g, '') : '');
                    }

                    // Chờ thêm 1 giây rồi gửi request fcollect
                    const fcollect = await new Promise(resolve => setTimeout(() => {
                        sendFormData(url + "?ngmar=fcl", claimData).then(resolve).catch(() => resolve(null));
                    }, 1000));

                    if (fcollect && fcollect.code && fcollect.code === 1) {
                        saveItem(item.name);
                        showToast("Bạn đã nhận được " + item.name);
                    } else {
                        showToast("Lỗi nhặt vật phẩm!");
                        if (getSetting("autoReload")) {
                            setTimeout(() => location.reload(), 3000);
                        }
                    }
                } else {
                    showToast("Lỗi lấy thông tin vật phẩm!");
                    if (getSetting("autoReload")) {
                        setTimeout(() => location.reload(), 3000);
                    }
                }
            }
            else {
                showToast("không có đồ nhặt!");
            }
        } catch (e) {
            console.error(e);
        }

        // Xóa nút "Nhặt bảo" nếu tồn tại
        const button = document.querySelector('.btn.btn-info');
        if (button && button.innerText === "Nhặt bảo") {
            button.remove();
        }
    };

    /* =================== INIT =================== */
    createShowButton();
    createSettingButton();
    setInterval(pollForItems, 30000); // Poll mỗi 30 giây

})();
