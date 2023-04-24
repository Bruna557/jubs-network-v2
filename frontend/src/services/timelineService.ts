import { API_GATEWAY_URL } from "./config"
import { TimelineResult } from "../types"

const HEADERS: HeadersInit = new Headers();
HEADERS.set("Authorization", `Bearer ${localStorage.getItem("token")}` || "")

export const fetchTimeline = async (username: string, postedOn: string): Promise<TimelineResult> => {
    console.log(postedOn)
    const url = `${API_GATEWAY_URL}/timeline/${username}?posted_on=${Date.parse(postedOn)}&scroll=down`
    return fetch(url, {
        method: "GET",
        headers: HEADERS
    })
    .then(response => {
        console.log(response)
        return response.json()
    })
    .then(data => {
        return data
    })
    .catch ((err) => {
        console.log("Error: unable to fetch posts", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}
