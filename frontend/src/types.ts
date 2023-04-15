export type Post = {
    username: string,
    posted_on: string,
    body: string,
    likes: number,
    picture: string
}

export type User = {
    username: string,
    bio: string,
    picture: string
    follow?: boolean
}

export type TimelineResult = {
    posts: Post[],
    has_more: boolean
}
