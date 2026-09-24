(function () {
    function showError(msg) {
        var link = document.getElementById('dclogin-link');
        var qrCode = document.getElementById('qr-code');
        var ctaSkel = document.getElementById('cta-skeleton');
        var qrSkel = document.getElementById('qr-skeleton');
        if (ctaSkel) ctaSkel.style.display = 'none';
        if (qrSkel) qrSkel.style.display = 'none';
        if (link) { link.textContent = msg; link.style.display = 'block'; link.style.pointerEvents = 'none'; }
        if (qrCode) { qrCode.innerHTML = '<p style="color:#888;padding:40px;text-align:center">' + msg + '</p>'; }
    }

    function generateProfile() {
        var ctaSkel = document.getElementById('cta-skeleton');
        var qrSkel = document.getElementById('qr-skeleton');
        var link = document.getElementById('dclogin-link');
        var qrLink = document.getElementById('qr-link');
        var qrLabel = document.getElementById('qr-label');

        fetch('/new')
            .then(function (r) {
                if (!r.ok) throw new Error('Ошибка сервера');
                return r.json();
            })
            .then(function (data) {
                var url = data.dclogin_url;
                link.href = url;
                link.style.display = 'block';
                qrLink.href = url;
                qrLink.style.display = 'block';
                if (qrLabel) qrLabel.style.display = 'block';
                if (ctaSkel) ctaSkel.style.display = 'none';
                if (qrSkel) qrSkel.style.display = 'none';
                var qrCode = document.getElementById('qr-code');
                var qr = new QRCode({ content: url, width: 300, height: 300, padding: 1, join: true });
                qrCode.innerHTML = qr.svg();
            })
            .catch(function (err) {
                showError('Не удалось создать профиль. Попробуйте позже.');
            });
    }
    generateProfile();
})();
