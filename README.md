# GitHub Action For Retrieving You Experiment With Allegro Trains


![GitHub stars](https://img.shields.io/github/stars/allegroai/trains?style=social)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/shomratalon/trains-get-stats/Get%20task%20stats)


Get your task results to your repo! 


This action will help you retrieve all Trains task results and post to Github discussion (issue or pull request). 

## Usage
### Workflow Example
This will add an action to your workflow that will comment the `TASK_ID` last metrics results to the current discussion. 

Will work in both github issues and github pull requests comments.

<img src="https://github.com/shomratalon/trains-get-stats/blob/master/docs/get_stats_flow.png?raw=true" width="100%">

```yaml
name: Get task stats
on: [issue_comment]

jobs:
  get-stats:
      if: contains(github.event.comment.body, '/get-stats')
      runs-on: ubuntu-latest
      steps:
        - name: Get task stats
          uses: shomratalon/trains-get-stats@master
          id: train
          with:
            TRAINS_API_ACCESS_KEY: ${{ secrets.ACCESS_KEY }}
            TRAINS_API_SECRET_KEY: ${{ secrets.SECRET_KEY }}
            TRAINS_API_HOST: ${{ secrets.TRAINS_API_HOST }}
            TASK_ID: "6f98c7d181b84327ae12e64537a97960"
          env:
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

#### Mandatory Inputs
  1. `TRAINS_API_ACCESS_KEY`: Your trains api access key. You can find it in your trains.conf file under api.credentials.access_key section, [read more](https://allegro.ai/docs/references/trains_ref/#api-section). 
  2. `TRAINS_API_SECRET_KEY`: Your trains api secret key. You can find it in your trains.conf file under api.credentials.secret_key section, [read more](https://allegro.ai/docs/references/trains_ref/#api-section).
  3. `TRAINS_API_HOST`: The Trains api server address. You can find it in your trains.conf file under  api.api_server section, [read more](https://allegro.ai/docs/references/trains_ref/#api-section).
  4. `TASK_ID`: Id of the task you would like to clone.
