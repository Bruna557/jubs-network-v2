import { URLS } from "./config"
import { User } from "../types"

const HEADERS: HeadersInit = new Headers()
HEADERS.set("Authorization", `Bearer ${localStorage.getItem("token")}` || "")

export const fetchUser = async (username: string): Promise<User> => {
    const url = `${URLS["user-service"]}/users/${username}`
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
    })
}

export const changeBio = async (username: string, bio: string) => {
    const url = `${URLS["user-service"]}/users/${username}`
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
    })
}

export const changePicture = async (username: string, picture: string) => {
    const url = `${URLS["user-service"]}/users/${username}`
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
    })
}

export const changePassword = async (username: string, password: string) => {
    const url = `${URLS["user-service"]}/users/${username}`
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
    })
}

export const login = async (username: string, password: string) => {
    const url = `${URLS["user-service"]}/auth/login`
    const headers: HeadersInit = new Headers()
    headers.set("Content-Type", "application/json")
    return fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({"username": username, "password": password})
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem("token", data.token)
        return true
    })
    .catch ((err) => {
        console.log("Error: unable to log in", err)
        return false
    })
}

export const register = async (username: string, password: string, bio: string, picture: string) => {
    const url = `${URLS["user-service"]}/users`
    return fetch(url, {
        method: "POST",
        headers: HEADERS,
        body: JSON.stringify({"username": username, "password": password, "bio": bio, "picture": picture})
    })
    .then(response => response.json())
    .then(data => {
        localStorage.setItem("token", data.token)
        return true
    })
    .catch ((err) => {
        console.log("Error: unable to register user", err)
        return false
    })
}

export const search = async (username: string): Promise<User[]> => {
    const url = `${URLS["user-service"]}/users?username=${username}`
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
    })
}