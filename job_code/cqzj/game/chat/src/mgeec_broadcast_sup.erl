%%% -------------------------------------------------------------------
%%% Author  : liurisheng
%%% Description :
%%%
%%% Created : 2010-08-03
%%% -------------------------------------------------------------------
-module(mgeec_broadcast_sup).

-behaviour(supervisor).
%% --------------------------------------------------------------------
%% Include files
%% --------------------------------------------------------------------

%% --------------------------------------------------------------------
%% External exports
%% --------------------------------------------------------------------
-export([start/0, start_link/0]).

%% --------------------------------------------------------------------
%% Internal exports
%% --------------------------------------------------------------------
-export([
	 init/1
        ]).

%% --------------------------------------------------------------------
%% Macros
%% --------------------------------------------------------------------
-define(SERVER, ?MODULE).

start() ->
    {ok, _Pid} = 
        supervisor:start_child(mgeec_sup,
                               {?MODULE, {?MODULE, start_link, []},
                                transient, infinity, supervisor, [?MODULE]}
                              ).

start_link() ->
    {ok, _Pid} = 
        supervisor:start_link({local, ?SERVER}, ?MODULE, []).

%% ====================================================================
%% Server functions
%% ====================================================================
%% --------------------------------------------------------------------
%% Func: init/1
%% Returns: {ok,  {SupFlags,  [ChildSpec]}} |
%%          ignore                          |
%%          {error, Reason}
%% --------------------------------------------------------------------
init([]) ->
    AChild = {mgeec_broadcast,{mgeec_broadcast,add_child_process,[]},
               transient,2000,worker,[mgeec_broadcast]},
    {ok,{{simple_one_for_one,10,10}, [AChild]}}.