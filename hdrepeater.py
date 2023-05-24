"""
HDRepeater: repeatedly create HDR images
"""
import sys
import pathlib

from radiance_pipeline.radiance_pipeline import radiance_pipeline
from radiance_pipeline.radiance_data import RadianceData

from helper import dict_merge, print_v, load_json, cp


def main() -> int:
    """ Main functionality """
    # Check argv
    if len(sys.argv) > 2:
        print("Too many args!")
        return 1
    if len(sys.argv) < 2:
        print("Too few args!")
        return 1

    # Load and run from argv[1]
    base_json = load_json(pathlib.Path(sys.argv[1]))
    print(base_json)
    run_base(base_json, pathlib.Path(sys.argv[1]).resolve())
    return 0


def run_base(base_json: dict, base_path: pathlib.Path =None) -> None:
    """ Run a base json """
    # Validate the base json and exit if bad
    if not validate_base(base_json, verbose=True):
        print("Error in base json")
        sys.exit()

    if base_path is not None:
        absoluteize_base(base_json, base_path)

    path_temp = pathlib.Path(base_json["path_temp"])
    path_output = pathlib.Path(base_json["path_output"])

    for run in base_json["runs"]:
        print(run["name"])

        # get default values
        run["params"] = dict_merge(run["params"], base_json["default"])

        # Check the run
        if not validate_run(run, verbose=True):
            print(f"Error in {run['name']}")
            continue
        if base_path is not None:
            absoluteize_run(run, base_path)

        params = run["params"]
        print(params)
        rd = RadianceData(diameter=params["diameter"],
                          crop_x_left=params["crop_x_left"],
                          crop_y_down=params["crop_y_down"],
                          view_angle_vertical=params["view_angle_vertical"],
                          view_angle_horizontal=params["view_angle_horizontal"],
                          target_x_resolution=params["target_x_resolution"],
                          target_y_resolution=params["target_y_resolution"],
                          paths_ldr=params["paths_ldr"],
                          path_temp=base_json["path_temp"],
                          path_rsp_fn=params["path_rsp_fn"],
                          path_vignetting=params["path_vignetting"],
                          path_fisheye=params["path_fisheye"],
                          path_ndfilter=params["path_ndfilter"],
                          path_calfact=params["path_calfact"],
                          path_errors=base_json["path_errors"],
                          path_logs=base_json["path_logs"])
        radiance_pipeline(rd)

        # Copy from temp to output, naming it runs["name"].hdr
        cp(str(path_temp.joinpath("output10.hdr")),
           str(path_output.joinpath(f"{run['name']}.hdr")))


def validate_base(base_json: dict, verbose: bool = False) -> bool:
    """ Returns true if stuff in base_json is valid """
    return True # TODO


def validate_run(run: dict, verbose: bool = False) -> bool:
    """ Returns true if params can be run by radiance pipeline """
    params = run["params"]

    # Validate values that have to be numbers
    for key in ["diameter", "crop_x_left", "crop_y_down", "view_angle_vertical",
                "view_angle_horizontal", "target_x_resolution", "target_y_resolution"]:
        val = params.get(key, None)
        if not isinstance(val, int):
            print_v(f"ERROR: Non-int type value spotted in {run['name']}: {key}={val}", verbose)
            return False

    # Validate ldr path
    if not isinstance(params["paths_ldr"], list) or not params["paths_ldr"]:
        print_v(f"ERROR: Empty ldr_paths spotted in {run['name']}", verbose)
        return False
    for item in params["paths_ldr"]:
        if not isinstance(item, str):
            print_v(f"ERROR: Non-string ldr path spotted in {run['name']}", verbose)
            return False

    # Validate defaultable paths
    for key in ["path_rsp_fn", "path_vignetting", "path_fisheye", "path_ndfilter", "path_calfact"]:
        val = params.get(key, None)
        if val is None:
            continue
        path = pathlib.Path(val)
        if not path.is_file():
            print_v(f"ERROR: bad file spotted in {run['name']}: {val}", verbose)
            return False
    return True


def absoluteize_run(run: dict, base_json_path: pathlib.Path) -> None:
    """ Make the parameters of run absolute to the base.
        Modifies run. """
    base_path = base_json_path.parent
    params = run["params"]
    for key in ["path_rsp_fn", "path_vignetting", "path_fisheye", "path_ndfilter", "path_calfact"]:
        if key not in params or params[key] is None:
            continue
        val = pathlib.Path(params[key])
        if not val.is_absolute():
            params[key] = str(base_path / val)

    # Absoluteize ldr images
    paths_ldr = params["paths_ldr"]
    for i,path in enumerate(paths_ldr):
        val = pathlib.Path(path)
        if not val.is_absolute():
            paths_ldr[i] = str(base_path / val)


def absoluteize_base(base, base_json_path: pathlib.Path) -> None:
    """ Make the parameters of base relative to base_path.
        Modifies base. """
    base_path = base_json_path.parent
    for key in ["path_temp", "path_output"]:
        val = pathlib.Path(base[key])
        if not val.is_absolute():
            base[key] = str(base_path / val)


if __name__ == "__main__":
    main()
