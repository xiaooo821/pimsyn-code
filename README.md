dse
- design_space_exploration2 修改后的，运行得到规定架构下的运行效率。
- design_space_exploration 运行得到选定网络的最佳架构

input：
prompt操作：   
conda activate pimsyn  
cd /Users/bamboo/Documents/PIMSYN/coding/PIMSYN-NN-1125    


任务：
1. 查看不同网络和不同总功率下的最佳功率效率差别
Alexnet：
python main.py --network ./models/JSON/alexnet.json  --total_power 25 --macro_setting unified --config config.json --output ./output/alexnet25.json 
python main.py --network ./models/JSON/alexnet.json  --total_power 49 --macro_setting unified --config config.json --output ./output/alexnet49.json 
resnet：
python main.py --network ./models/JSON/resnet18.json  --total_power 49 --macro_setting unified --config config.json --output ./output/resnet.json 
python main.py --network ./models/JSON/resnet18.json  --total_power 24.5 --macro_setting unified --config config.json --output ./output/resnet.json 

vgg13
python main.py --network ./models/JSON/vgg13.json  --total_power 115 --macro_setting unified --config config.json --output ./output/vgg13_115.json 
python main.py --network ./models/JSON/vgg13.json  --total_power 230 --macro_setting unified --config config.json --output ./output/vgg13_230.json 
msra ：
python main.py --network ./models/JSON/msra_A.json  --total_power 132 --macro_setting unified --config config.json --output ./output/msra_A132.json 
python main.py --network ./models/JSON/msra_A.json  --total_power 264 --macro_setting unified --config config.json --output ./output/msra_A264.json 
vgg16 ：
python main.py --network ./models/JSON/vgg16.json  --total_power 132 --macro_setting unified --config config.json --output ./output/vgg16_132.json 
python main.py --network ./models/JSON/vgg16.json  --total_power 264 --macro_setting unified --config config.json --output ./output/vgg16_264.json 

注意啊，命令行输入的total_power也要用之前网络的数据。

用vgg13的跑其他网络：
Alexnet：
python main.py --network ./models/JSON/alexnet.json  --total_power 115 --macro_setting unified --config config.json --use_existing_config ./output/vgg13_115.json --output ./output/preset_config/vgg13_alex.json
vgg13：
python main.py --network ./models/JSON/vgg13.json  --total_power 115 --macro_setting unified --config config.json --use_existing_config ./output/vgg13_115.json --output ./output/preset_config/vgg13_vgg13.json
msra:
python main.py --network ./models/JSON/msra_A.json  --total_power 115 --macro_setting unified --config config.json --use_existing_config ./output/vgg13_115.json --output ./output/preset_config/vgg13_msra.json
vgg16；
python main.py --network ./models/JSON/vgg16.json  --total_power 115 --macro_setting unified --config config.json --use_existing_config ./output/vgg13_115.json --output ./output/preset_config/vgg13_vgg16.json
resnet:
python main.py --network ./models/JSON/resnet18.json  --total_power 115 --macro_setting unified --config config.json --use_existing_config ./output/vgg13_115.json --output ./output/preset_config/vgg13_resnet.json


最后运行python draw.py绘制组合图。

