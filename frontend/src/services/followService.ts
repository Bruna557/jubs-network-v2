import { URLS } from "./config"
import { User } from "../types"

const HEADERS: HeadersInit = new Headers();
HEADERS.set("Authorization", `Bearer ${localStorage.getItem("token")}` || "")

export const fetchRecommendation = async (username: string): Promise<User[]> => {
    const url = `${URLS["follow-service"]}/followers/recommendation/${username}?page_size=7&page_number=1`
    return fetch(url, {
        method: "GET",
        headers: HEADERS
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch ((err) => {
        console.log("Error: unable to fetch recommendation", err)
        if (err.response.status == 401) {
            throw new Error("Unauthorized");
        }
    })
}

export const follow = async (username: string, followed:string) => {
    const url = `${URLS["follow-service"]}/follow/${username}/${followed}`
    return fetch(url, {
        method: "POST",
        headers: HEADERS
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch ((err) => {
        console.log("Error: unable to follow", err)
        if (err.response.status == 401) {
            throw new Error("Unauthorized");
        }
    })
}
