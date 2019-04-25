export function buildURLQuery(path, params) {
    let url = new URL(`${window.location.origin}${path}`);
    url.search = new URLSearchParams(params);
    return url
}