export const post = async (username: string, body: string) => {
    console.log(username + " posted: " + body)
}

export const like = async (username: string, postedOn: string) => {
    console.log("new like")
}
