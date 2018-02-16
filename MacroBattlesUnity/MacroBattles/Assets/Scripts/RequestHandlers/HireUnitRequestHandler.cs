using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

#if UNITY_EDITOR
using UnityEditor;
#endif

public class HireUnitRequestHandler {

  private static string requestDomain = Constants.APP_DOMAIN;

  public static IEnumerator HireUnit(string unitTypeString) {
    Debug.Log("HireUnit" + unitTypeString);
  // TODO: create a common request handler class that all others extend, which has this set.
#if UNITY_EDITOR
    if (EditorApplication.isPlayingOrWillChangePlaymode) {
      requestDomain = Constants.LOCAL_HOST;
    }
#endif
    // TODO: Error check the GameState first.
    string query = "/hire-unit";
    HireUnitRequestModel model = new HireUnitRequestModel();
    model.unit_type_string = unitTypeString;
    model.player_id = GameState.GetCurrentPlayerKey();

    using(UnityWebRequest www = UnityWebRequest.Put(
        requestDomain + query, JsonUtility.ToJson(model))) {
      www.SetRequestHeader("Content-Type", "application/json");
      yield return www.SendWebRequest();

      if(www.isNetworkError) {
        // TODO: Make this show an error on the client, or something.
        Debug.LogError(www.error);
      } else {
        string rawjson = www.downloadHandler.text;
        ResponseModel response = JsonUtility.FromJson<ResponseModel>(rawjson);
        if (response.status == ResponseConstants.SUCCESS) {
          // TODO: Handle a response from the server.
          Debug.Log(response.data);

          if (response.data == "unit too expensive") {
            // TODO: show cost of unit to user and their money amount.

          } else { // TODO: update map to show new unit.

          }

        } else {
          // TODO: If getting the map doesn't work, expose the Error Message to the user.
          Debug.Log(response.status);
          Debug.Log(response.data);
          Debug.Log(response.error);
        }
      }
    }
  }
}
