import instaloader
import json


def download_media(url):
    L = instaloader.Instaloader()

    if url[-1] != "/":
        url=url+"/"
    if url.find("https://www.instagram.com") == -1:
        print("Ce n'est pas un lien Instagram")
        return
    shortcode = url.split("/")[-2]
    # Récupérer les informations sur le poste à partir du code court
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    if post.is_video:
        print("Téléchargement de la vidéo...")
        L.download_videos=False
        L.save_metadata=False
        L.download_comments=False
        # Téléchargement du média associé
        # L.download_post(post, target=shortcode)
        info={"photoURL":post.url,"videoURL":post.video_url,"videoDuration":post.video_duration}
        return json.dumps(info)
    else:
        print("This not a video")
        return
# Exemple d'utilisation avec le code court du post
# download_media("https://www.instagram.com/p/CEf6eWzF7y9/", "instagram")
