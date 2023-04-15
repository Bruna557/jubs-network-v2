import { URLS } from "./config"

const HEADERS: HeadersInit = new Headers();
HEADERS.set("Authorization", `Bearer ${localStorage.getItem("token")}` || "")

export const post = async (username: string, body: string) => {
    const url = `${URLS["post-service"]}/posts/${username}`
    return fetch(url, {
        method: "POST",
        headers: HEADERS,
        body: JSON.stringify({"body": body})
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
}

export const like = async (username: string, postedOn: string) => {
    const url = `${URLS["post-service"]}/likes/${username}/${Date.parse(postedOn)}`
    return fetch(url, {
        method: "PUT",
        headers: HEADERS
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
}
