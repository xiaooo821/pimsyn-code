import argparse
import json
import math
from multiprocessing import Pool, Manager

from onnxruntime.transformers.bert_test_data import output_test_data

from frontend import FrontEnd
from dse import design_space_exploration,design_space_exploration2


DEFAULT_XBAR_SIZE = [128, 256, 512]
DEFAULT_RRAM_RESOLUTION = [1, 2, 4]
DEFAULT_RRAM_RATIO = [0.15, 0.2, 0.25, 0.3]

# 将epe_result以json形式存入文件output_path中
def save_result_to_json(res, output_path):

    with open(output_path, 'w') as f:
        json.dump(res, f,indent=4)

def print_accelerator_configuration(arch, file_path):

    del arch['gene']
    del arch['dup']
    del arch['xbar_alloc']
    with open(file_path, "w") as file:
        json.dump(arch, file, indent=4)


def print_pimcomp_configuration(arch, file_path):

    pimcomp_cfg = {
        "CellPrecision": arch['rram_res'],
        "CrossbarH": arch['xbar_size'],
        "CrossbarW": arch['xbar_size'],
    }

    for value in arch.values():
        if isinstance(value, dict) and 'macro_size' in value.keys():
            macro_size = value['macro_size']
            break

    pimcomp_cfg['ChipH'] = arch['macro_h']
    pimcomp_cfg['ChipW'] = arch['macro_w']
    pimcomp_cfg['CoreH'] = math.ceil(math.sqrt(macro_size))
    pimcomp_cfg['CoreW'] = math.ceil(macro_size/pimcomp_cfg['CoreH'])

    with open(file_path, "w") as file:
        json.dump(pimcomp_cfg, file, indent=4)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Please specify the PIMSYN arguments")
    parser.add_argument('--onnx_path', '-onnx',
                        type=str,
                        default=None,
                        help='Specify the path of neural network onnx file')
    parser.add_argument('--network', '-n',
                        type=str,
                        required=True,
                        help='Specify the output path of onnx2json frontend')
    parser.add_argument('--total_power', '-p',
                        type=float,
                        default=0,
                        # required=True,
                        help='Specify the peak power limitation')
    parser.add_argument('--macro_setting', '-m',
                        type=str,
                        default='unified',
                        choices=['unified', 'specified'],
                        help='Possible values: unified, specified')
    parser.add_argument('--config', '-cfg',
                        type=str,
                        required=True,
                        help='Specify configuration file path'
                        )
    parser.add_argument('--macro_reuse', '-r',
                        type=bool,
                        default=False,
                        help='Whether enable inter-layer macro sharing')
    parser.add_argument('--output', '-o',
                        type=str,
                        default="./output/pimsyn.json",
                        help='Output file path')
    parser.add_argument('--pimcomp',
                        type=str,
                        default="./output/pimcomp.json",
                        help='The path of input arguments for PIMCOMP')
    #新增
    parser.add_argument('--use_existing_config',
                        type=str,
                        default=None,
                        help='Path or identifier of existing optimal configuration to use')


    args = parser.parse_args()
    config_file = open(args.config, 'r')
    pimsyn_cfg = json.load(config_file)
    pimsyn_cfg.update(vars(args)) # 把命令行输入存进来
    if args.onnx_path:
        frontend = FrontEnd(args.onnx_path, args.network)
        frontend.run()

    arch_candidates = []

    manager = Manager()
    shared_cfg = manager.dict(pimsyn_cfg)

    upload_config = {}
    if args.use_existing_config: #如果用已有的配置跑程序的话
        with open(args.use_existing_config,'r') as file:
            upload_config=json.load(file)
            pimsyn_cfg.update(upload_config)
        # epe efficient power efficiency
        result=design_space_exploration2(pimsyn_cfg["rram_ratio"],
                                 pimsyn_cfg["rram_res"],
                                 pimsyn_cfg["xbar_size"],
                                            pimsyn_cfg)
        print("efe of current CNN network using existed parameter is: ",result["epe"])
        # 输出到output文件中
        output_path=args.output
        save_result_to_json(result, args.output)



    else:
        with Pool() as pool:
            for rram_ratio in DEFAULT_RRAM_RATIO:
                for rram_res in DEFAULT_RRAM_RESOLUTION:
                    for xbar_size in DEFAULT_XBAR_SIZE:
                        result = pool.apply_async(design_space_exploration,
                                                  args=(rram_ratio,
                                                        rram_res,
                                                        xbar_size,
                                                        shared_cfg))
                        arch_candidates.append(result)
            pool.close()
            pool.join()

        best_power_efficiency = -1
        best_arch = None
        for candidate in arch_candidates:
            arch = candidate.get()
            if arch['power_efficiency'] > best_power_efficiency:
                best_arch = arch
                best_power_efficiency = arch['power_efficiency']
        if best_arch:
            print(f"最佳架构的功率效率为: {best_power_efficiency}")
            if args.macro_setting == 'unified':
                print_pimcomp_configuration(best_arch, args.pimcomp)
            print_accelerator_configuration(best_arch, args.output)
