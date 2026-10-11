import kagglehub

path = kagglehub.dataset_download(
    "shashwatwork/dataco-smart-supply-chain-for-big-data-analysis"
)
print("Путь к файлам:", path)