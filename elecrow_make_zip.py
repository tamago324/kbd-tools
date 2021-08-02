from pathlib import Path
import re
import sys
import shutil


conv_dict = {
    r"(.*)-F_Cu\.gbr$":  ".GTL",
    r"(.*)-B_Cu\.gbr$":  ".GBL",
    r"(.*)-F_Mask\.gbr$":  ".GTS",
    r"(.*)-B_Mask\.gbr$":  ".GBS",
    r"(.*)-F_SilkS\.gbr$":  ".GTO",
    r"(.*)-B_SilkS\.gbr$":  ".GBO",
    r"(.*)-PTH\.drl$":  ".TXT",
    r"(.*)-NPTH\.drl$":  "-NPTH.TXT",
    r"(.*)-Edge_Cuts.gbr$":  ".GML",
}

def main():
    args = sys.argv

    if len(args) != 3:
        print("python3 elecrow_conv.py [gbr_dir_path] [zip_name]")
        return

    path = Path(args[1])
    zip_name = Path(args[2]).stem

    # zip用のディレクトリを作成する
    zip_temp_path = (path / (zip_name + '_temp'))
    zip_temp_path.mkdir()

    # コピーする
    for x in path.iterdir():
        for pattern, postfix in conv_dict.items():
            m = re.match(pattern, x.name)
            if m is None:
                continue

            name = m.groups()[0]
            shutil.copy(x, zip_temp_path / (name + postfix))


    # zipに固める
    zip_path = (path / zip_name)
    shutil.make_archive(zip_path.absolute(), 'zip', root_dir=zip_temp_path)

    # 削除
    shutil.rmtree(zip_temp_path.absolute())

if __name__ == '__main__':
    main()
