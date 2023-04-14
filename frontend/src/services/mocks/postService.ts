export const post = async (username: string, body: string) => {
    console.log(username + " posted: " + body)
}

export const like = async (username: string, createdOn: string) => {
    console.log("new like")
}
