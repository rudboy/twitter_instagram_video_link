import requests

def api_twitter(id):
    try:
        # Effectuer une requête GET pour obtenir le jeton invité (gt)
        response = requests.get('https://twitter.com/TweetsOfCats/', headers={
            'authority': 'twitter.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        })
        response.raise_for_status()
        response_data = response.text
        start_index = response_data.find('"gt=') + 4
        end_index = response_data.find(';', start_index)
        gt = response_data[start_index:end_index]
    except Exception as err:
        print(err)
        return {'message': 'could not get guest token'}

    try:
        # Effectuer une requête GET pour obtenir les informations du tweet
        variables = '{"tweetId":"' + id + '","withCommunity":false,"includePromotedContent":false,"withVoice":false}'
        features = '{"creator_subscriptions_tweet_preview_api_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"responsive_web_home_pinned_timelines_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"responsive_web_media_download_video_enabled":false,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_enhance_cards_enabled":false}'
        headers = {
            'authority': 'twitter.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'content-type': 'application/json',
            'referer': 'https://twitter.com/TweetsOfCats/status/1710629064757608670',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'x-guest-token': gt,
            'x-twitter-active-user': 'yes',
            'x-twitter-client-language': 'en',
        }
        response = requests.get(f'https://twitter.com/i/api/graphql/mbnjGF4gOwo5gyp9pe5s4A/TweetResultByRestId?variables={variables}&features={features}', headers=headers)
        response.raise_for_status()
        tweet = response.json()
    except Exception as err:
        return {'message': 'tweet not found'}

    try:
        # Extraire les informations vidéo du tweet
        entities = tweet['data']['tweetResult']['result']['legacy']['extended_entities']['media']
        for entity in entities:
            if 'video_info' in entity and 'variants' in entity['video_info']:
                return {
                    'videoURL': entity['video_info']['variants'][-1].get("url"),
                    'photoURL': entity['media_url_https'],
                    'videoDuration': entity['video_info']['duration_millis']
                }
    except Exception as err:
        return {'message': 'no video'}

    return {'message': 'no video'}
