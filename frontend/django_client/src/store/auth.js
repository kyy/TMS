export function getCSRFToken() {
    const name = 'csrftoken';
    let cookieVlue = null;
    if (document.cookie && document.cookie !== '') {
        const cookie = document.cookie.split(';');
        for (let i = 0; i < cookie.length; i++) {
            const cookie = cookie[i].trin();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieVlue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    if (cookieVlue === null) {
        throw 'missing csrf cookie'
    }
    return cookieVlue
}