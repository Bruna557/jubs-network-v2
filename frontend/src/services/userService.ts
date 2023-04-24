import { API_GATEWAY_URL } from "./config"
import { User, UsersResult } from "../types"

const HEADERS: HeadersInit = new Headers()
HEADERS.set("Authorization", `Bearer ${localStorage.getItem("token")}` || "")

export const fetchUser = async (username: string): Promise<User> => {
    const url = `${API_GATEWAY_URL}/users/${username}`
    return fetch(url, {
        method: "GET",
        headers: HEADERS
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch ((err) => {
        console.log("Error: unable to fetch user", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}

export const changeBio = async (username: string, bio: string) => {
    const url = `${API_GATEWAY_URL}/users/${username}`
    HEADERS.set("Content-Type", "application/json")
    return fetch(url, {
        method: "PUT",
        headers: HEADERS,
        body: JSON.stringify({"bio": bio})
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch ((err) => {
        console.log("Error: unable to change bio", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}

export const changePicture = async (username: string, picture: string) => {
    const url = `${API_GATEWAY_URL}/users/${username}`
    HEADERS.set("Content-Type", "application/json")
    return fetch(url, {
        method: "PUT",
        headers: HEADERS,
        body: JSON.stringify({"picture": picture})
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch ((err) => {
        console.log("Error: unable to change picture", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}

export const changePassword = async (username: string, password: string) => {
    const url = `${API_GATEWAY_URL}/users/${username}`
    HEADERS.set("Content-Type", "application/json")
    return fetch(url, {
        method: "PUT",
        headers: HEADERS,
        body: JSON.stringify({"password": password})
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch ((err) => {
        console.log("Error: unable to change password", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}

export const login = async (username: string, password: string) => {
    const url = `${API_GATEWAY_URL}/auth/login`
    const headers: HeadersInit = new Headers()
    headers.set("Content-Type", "application/json")
    return fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({"username": username, "password": password})
    })
    .then(response => response.json())
    .then(data => {
        return data.token
    })
    .catch ((err) => {
        console.log("Error: unable to log in", err)
    })
}

export const register = async (username: string, password: string, bio: string, picture: string) => {
    const url = `${API_GATEWAY_URL}/users`
    const headers: HeadersInit = new Headers()
    headers.set("Content-Type", "application/json")
    return fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({"username": username, "password": password, "bio": bio, "picture": picture})
    })
    .then(response => response.json())
    .then(data => {
        return data.token
    })
    .catch ((err) => {
        console.log("Error: unable to register user", err)
    })
}

export const search = async (username: string, q: string, page_number: number): Promise<UsersResult> => {
    const url = `${API_GATEWAY_URL}/users/${username}/search?q=${q}&page_size=10&page_number=${page_number}`
    return fetch(url, {
        method: "GET",
        headers: HEADERS
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch ((err) => {
        console.log("Error: unable to search", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}

export const fetchRecommendation = async (username: string): Promise<UsersResult> => {
    const url = `${API_GATEWAY_URL}/followers/recommendation/${username}?page_size=7&page_number=1`
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
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}

export const follow = async (username: string, followed:string) => {
    const url = `${API_GATEWAY_URL}/follow/${username}/${followed}`
    return fetch(url, {
        method: "POST",
        headers: HEADERS
    })
    .then(response => {
        return response
    })
    .catch ((err) => {
        console.log("Error: unable to follow", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}

export const unfollow = async (username: string, followed:string) => {
    const url = `${API_GATEWAY_URL}/follow/${username}/${followed}`
    return fetch(url, {
        method: "DELETE",
        headers: HEADERS
    })
    .then(response => {
        return response
    })
    .catch ((err) => {
        console.log("Error: unable to follow", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}

export const fetchFollowers = async (username: string, page_number: number): Promise<UsersResult> => {
    const url = `${API_GATEWAY_URL}/followers/${username}?page_size=10&page_number=${page_number}`
    return fetch(url, {
        method: "GET",
        headers: HEADERS
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch ((err) => {
        console.log("Error: unable to follow", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}

export const fetchFollowing = async (username: string, page_number: number): Promise<UsersResult> => {
    const url = `${API_GATEWAY_URL}/followings/${username}?page_size=10&page_number=${page_number}`
    return fetch(url, {
        method: "GET",
        headers: HEADERS
    })
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch ((err) => {
        console.log("Error: unable to follow", err)
        if (err.response.status === 401) {
            throw new Error("Unauthorized");
        }
    })
}
