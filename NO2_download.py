import requests
import concurrent.futures  # For multi-threading IO and multi-processing

# %%
data_folder = 'NO2/'
link_lists = []
with open('NO2/subset_OMNO2d_003_20200419_135250.txt') as file:
    for line in file:
        line = line.strip()
        link_lists.append(line)

link_lists = link_lists[2:]


def download_NO2(url):
    with requests.get(url) as response:
        name = url.split('/')[-1].split('?')[0]
        with open(data_folder + name, 'wb') as f:
            f.write(response.content)
            print(f'{name} was downloaded...')


# %% Multi-threading IO for downloading files
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_NO2, link_lists)
