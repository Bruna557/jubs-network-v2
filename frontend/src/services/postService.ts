import { API_GATEWAY_URL } from "./config"
import { Post } from "../types";

const HEADERS: HeadersInit = new Headers();
HEADERS.set("Authorization", `Bearer ${localStorage.getItem("token")}` || "")

export const post = async (username: string, body: string, picture: string): Promise<Post> => {
    const url = `${API_GATEWAY_URL}/posts/${username}`
    HEADERS.set("Content-Type", "application/json")
    return fetch(url, {
        method: "POST",
        headers: HEADERS,
        body: JSON.stringify({"body": body, "picture": picture})
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch ((err) => {
        console.log("Error: unable to create post", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}

export const like = async (username: string, postedOn: string) => {
    const url = `${API_GATEWAY_URL}/likes/${username}/${Date.parse(postedOn)}`
    return fetch(url, {
        method: "PUT",
        headers: HEADERS
    })
    .then(response => {
        return response
    })
    .catch ((err) => {
        console.log("Error: unable to like post", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}
