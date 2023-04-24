import { Post } from "../../types"

export const post = async (username: string, body: string, picture: string): Promise<Post> => {
    return new Promise((resolve, reject) => {
        resolve({
            username: username,
            body: body,
            likes: 0,
            picture: "https://cdn-icons-png.flaticon.com/512/5968/5968350.png",
            posted_on: " " + (new Date()).toString()
        })
    })
}

export const like = async (username: string, postedOn: string): Promise<string> => {
    return new Promise((resolve, reject) => {
        resolve("OK")
    })
}
