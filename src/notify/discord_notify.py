import requests
from builder.builder import Build
from datetime import datetime


def discord_notify(build: Build, hook_url: str):
    title = ''
    if build.success:
        color = 2031360
        title = f'✅ Build Success for {build.repository} on {build.branch} ✅'
    else:
        color = 16711680
        title = f'❌ Build Failed for {build.repository} on {build.branch} ❌'

    # use hyperlink with commit message linking to commit url
    commit_url_formatted = f'[{build.commit_message}]({build.commit_url})'
    # format day/month/year hour:minute:second
    formatted_date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    embed = {
        'title': title,
        'fields': [
            {
                'name': 'Build Time',
                'value': f'{round(build.build_time, 2)} seconds',
                'inline': False
            },
            {
                'name': 'Commit URL',
                'value': commit_url_formatted,
                'inline': False
            },
            {
                'name': 'Committer',
                'value': f'Name: {build.committer.name}\n' /
                         'Email: {build.committer.email}\n' /
                         'Username: {build.committer.username}',
                'inline': False
            },
        ],
        'color': color,
        'footer': {
            'text': formatted_date
        }
    }

    if not build.success:
        embed['fields'].append({
            'name': 'Stage',
            'value': build.stage,
            'inline': False
        })
        embed['fields'].append({
            'name': 'Error',
            'value': build.error,
            'inline': False
        })

    data = {
        'embeds': [embed],
    }
    requests.post(hook_url, json=data)
