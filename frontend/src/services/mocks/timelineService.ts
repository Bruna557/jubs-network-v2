import { Post } from "../../types"

let posts = [
    {
        "username": "bruna",
        "posted_on": "Sat, 29 Apr 2023 18:38:08 GMT",
        "body": "Quisque vel ligula feugiat, viverra lorem et, pellentesque lacus. Vestibulum hendrerit posuere euismod. Maecenas scelerisque, arcu et malesuada auctor, nulla justo efficitur sem, non ultricies risus mauris vitae sem.",
        "likes": 10,
        "picture": "https://cdn-icons-png.flaticon.com/512/5968/5968350.png"
    },
    {
        "username": "ryuk",
        "posted_on": "Sat, 29 Apr 2023 17:29:31 GMT",
        "body": "Etiam eu augue ut tortor commodo tempus at sit amet velit. Cras consectetur dolor neque, vel finibus augue porta eu. Phasellus turpis felis, bibendum vitae risus nec, mattis convallis sapien. Suspendisse eget sapien sed lorem facilisis dapibus at et sem. Duis a ultrices turpis.",
        "likes": 5,
        "picture": "https://cdn-icons-png.flaticon.com/512/415/415682.png"
    },
    {
        "username": "ryuk",
        "posted_on": "Sat, 29 Apr 2023 16:19:04 GMT",
        "body": "Vestibulum finibus ligula iaculis magna pharetra, a lobortis nibh condimentum. Nunc tellus neque, pretium quis maximus sit amet, sollicitudin at metus.",
        "likes": 124,
        "picture": "https://cdn-icons-png.flaticon.com/512/415/415682.png"
    },
    {
        "username": "jubs",
        "posted_on": "Sat, 29 Apr 2023 16:08:27 GMT",
        "body": "Pellentesque nisl mi, bibendum nec tempus non, tempus ac massa. In condimentum laoreet rutrum. Pellentesque vestibulum orci nibh, in posuere nisi luctus a. Curabitur id pretium nunc. Pellentesque quis urna non nisl tempus euismod gravida in sem.",
        "likes": 26,
        "picture": "https://cdn-icons-png.flaticon.com/512/8876/8876508.png"
    },
    {
        "username": "ryuk",
        "posted_on": "Sat, 29 Apr 2023 16:07:23 GMT",
        "body": "Vestibulum in turpis dictum, pulvinar arcu non, euismod arcu. Maecenas quis dui vitae magna aliquet cursus sed non purus. Curabitur ornare elementum pellentesque. Quisque in cursus quam. Donec at mattis tellus, nec consequat diam.",
        "likes": 268,
        "picture": "https://cdn-icons-png.flaticon.com/512/415/415682.png"
    }
]

export const fetchTimeline = async (username: string): Promise<Post[]> => {
    return new Promise((resolve, reject) => {
        resolve(posts)
    })
}
