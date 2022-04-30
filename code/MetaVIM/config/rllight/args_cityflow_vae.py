import argparse

import torch
import os

from utils.cli import boolean_argument
from dict_and_info import *
# ------------------------ raw ------------------------
def get_args_3_3_raw():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_3_3_raw)
    parser.add_argument("--infos", type=str, default=infos_3_3)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSpolicy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_6_6_raw():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_6_6_raw)
    parser.add_argument("--infos", type=str, default=infos_6_6)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSpolicy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_10_10_raw():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_10_10_raw)
    parser.add_argument("--infos", type=str, default=infos_10_10)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='model/policy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='model/encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='model/reward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='model/reward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='model/state_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='model/state_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_3_4_raw():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_3_4_raw)
    parser.add_argument("--infos", type=str, default=infos_3_4)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False, 
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='model/policy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='model/encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='model/reward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='model/reward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='model/state_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='model/state_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_4_4_raw():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_4_4_raw)
    parser.add_argument("--infos", type=str, default=infos_4_4)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='model/policy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='model/encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='model/reward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='model/reward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='model/state_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='model/state_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_16_3_raw():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_16_3_raw)
    parser.add_argument("--infos", type=str, default=infos_16_3)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSpolicy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args


# ------------------------ 2570 ------------------------
def get_args_3_3_2570():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_3_3_2570)
    parser.add_argument("--infos", type=str, default=infos_3_3)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSpolicy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_6_6_2570():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_6_6_2570)
    parser.add_argument("--infos", type=str, default=infos_6_6)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSpolicy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_10_10_2570():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_10_10_2570)
    parser.add_argument("--infos", type=str, default=infos_10_10)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='model/policy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='model/encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='model/reward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='model/reward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='model/state_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='model/state_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_3_4_2570():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_3_4_2570)
    parser.add_argument("--infos", type=str, default=infos_3_4)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='model/policy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='model/encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='model/reward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='model/reward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='model/state_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='model/state_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_4_4_2570():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_4_4_2570)
    parser.add_argument("--infos", type=str, default=infos_4_4)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='model/policy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='model/encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='model/reward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='model/reward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='model/state_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='model/state_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_16_3_2570():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_16_3_2570)
    parser.add_argument("--infos", type=str, default=infos_16_3)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSpolicy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args





# ------------------------ 4770 ------------------------
def get_args_3_3_4770():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_3_3_4770)
    parser.add_argument("--infos", type=str, default=infos_3_3)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSpolicy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_6_6_4770():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_6_6_4770)
    parser.add_argument("--infos", type=str, default=infos_6_6)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSpolicy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_10_10_4770():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_10_10_4770)
    parser.add_argument("--infos", type=str, default=infos_10_10)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='model/policy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='model/encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='model/reward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='model/reward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='model/state_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='model/state_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_3_4_4770():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_3_4_4770)
    parser.add_argument("--infos", type=str, default=infos_3_4)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='model/policy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='model/encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='model/reward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='model/reward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='model/state_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='model/state_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_4_4_4770():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_4_4_4770)
    parser.add_argument("--infos", type=str, default=infos_4_4)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='model/policy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='model/encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='model/reward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='model/reward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='model/state_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='model/state_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args

def get_args_16_3_4770():
    parser = argparse.ArgumentParser()

    # --- GENERAL ---
    parser.add_argument("--memo", type=str, default='meta_vim')
    parser.add_argument("--env", type=int, default=1)  # env=1 means you will run CityFlow
    parser.add_argument("--gui", type=bool, default=True)
    parser.add_argument("--road_net", type=str, default='4_4') # attention
    parser.add_argument("--volume", type=str, default='hangzhou') # attention # hangzhou # 300
    parser.add_argument("--suffix", type=str, default="real") # attention # real 0.3_bi
    parser.add_argument("--mod", type=str, default='meta_vim')  # SimpleDQN, SimpleDQNOne, GCN, CoLight, Lit
    parser.add_argument("--cnt",type=int, default=3600)  # 3600
    parser.add_argument("--gen",type=int, default=1)  # 4
    parser.add_argument("-all", action="store_true", default=True)
    parser.add_argument("--workers",type=int, default=7)
    parser.add_argument("--onemodel",type=bool, default=False)
    parser.add_argument("--gpu", type=str, default="-1")
    parser.add_argument("--path_to_log", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test/train_round") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test/train
    parser.add_argument("--path_to_work_directory", type=str, default="/home/zlw/PycharmProjects/meta_vim/records/test/hangzhou_test") # attention /home/zlw/PycharmProjects/meta_vim/records/test/3_3_test
    parser.add_argument("--dic_traffic_env_conf", type=str, default=dic_traffic_env_conf_16_3_4770)
    parser.add_argument("--infos", type=str, default=infos_16_3)

    # training parameters
    # parser.add_argument('--num_frames', type=int, default=1e8, help='number of frames to train')
    parser.add_argument('--max_rollouts_per_task', type=int, default=4)

    # MetaVIM
    parser.add_argument('--exp_label', default='metavim', help='label for the experiment')
    parser.add_argument('--disable_metavim', type=boolean_argument, default=False,
                        help='Train policy w/o MetaVIM architecture')

    # env
    parser.add_argument('--env_name', default='Cityflow', help='environment to train on')
    parser.add_argument('--norm_obs_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--norm_rew_for_policy', type=boolean_argument, default=False)
    parser.add_argument('--normalise_actions', type=boolean_argument, default=False, help='output normalised actions')

    # --- POLICY ---

    # network
    parser.add_argument('--policy_layers', nargs='+', default=[32, 32])
    parser.add_argument('--policy_activation_function', type=str, default='tanh')

    # algo
    parser.add_argument('--policy', type=str, default='ppo', help='choose: a2c, ppo, optimal, oracle')

    parser.add_argument('--ppo_num_epochs', type=int, default=100, help='ppo_num_epochs(default: 100)')
    parser.add_argument('--ppo_num_minibatch', type=int, default=16, help="ppo_num_minibatch(default: 16)")
    parser.add_argument('--ppo_use_huberloss', type=boolean_argument, default=True, help='ppo_use_huberloss(default: True)')
    parser.add_argument('--ppo_use_clipped_value_loss', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')
    parser.add_argument('--ppo_clip_param', type=boolean_argument, default=True, help='ppo_use_clipped_value_loss(default: True)')

    # a2c specific
    parser.add_argument('--a2c_alpha', type=float, default=0.99, help='RMSprop optimizer alpha (default: 0.99)')

    # other hyperparameters
    parser.add_argument('--lr_policy', type=float, default=0.0007, help='learning rate (default: 7e-4)')
    parser.add_argument('--policy_num_steps', type=int, default=60, # 60
                        help='number of env steps to do (per process) before updating (for A2C ~ 10, for PPO ~100)')
    parser.add_argument('--policy_eps', type=float, default=1e-5, help='optimizer epsilon (1e-8 for ppo, 1e-5 for a2c)')
    parser.add_argument('--policy_init_std', type=float, default=1.0)
    parser.add_argument('--policy_value_loss_coef', type=float, default=0.5,
                        help='value loss coefficient (default: 0.5)')
    parser.add_argument('--policy_entropy_coef', type=float, default=0.1,
                        help='entropy term coefficient (default: 0.01)')
    parser.add_argument('--policy_gamma', type=float, default=0.95, help='discount factor for rewards (default: 0.99)')
    parser.add_argument('--policy_use_gae', type=boolean_argument, default=True,
                        help='use generalized advantage estimation')
    parser.add_argument('--policy_tau', type=float, default=0.95, help='gae parameter (default: 0.95)')
    parser.add_argument('--use_proper_time_limits', type=boolean_argument, default=False)
    parser.add_argument('--policy_max_grad_norm', type=float, default=0.5, help='max norm of gradients (default: 0.5)')
    parser.add_argument('--precollect_len', type=int, default=5000,
                        help='how many frames to pre-collect before training begins')

    # --- VAE TRAINING ---

    # general
    parser.add_argument('--lr_vae', type=float, default=0.001)
    parser.add_argument('--size_vae_buffer', type=int, default=100000,
                        help='how many trajectories to keep in VAE buffer')
    parser.add_argument('--vae_buffer_add_thresh', type=float, default=1, help='prob of adding a new traj to buffer')
    parser.add_argument('--vae_batch_num_trajs', type=int, default=25,
                        help='how many trajectories to use for VAE update')
    parser.add_argument('--vae_batch_num_enc_lens', type=int, default=None,
                        help='for how many timesteps to compute the ELBO; None uses all')
    parser.add_argument('--num_vae_updates', type=int, default=3,
                        help='how many VAE update steps to take per meta-iteration')
    parser.add_argument('--pretrain_len', type=int, default=0, help='for how many updates to pre-train the VAE')
    parser.add_argument('--kl_weight', type=float, default=1, help='weight for the KL term')

    # - encoder
    parser.add_argument('--latent_dim', type=int, default=5, help='dimensionality of latent space')
    parser.add_argument('--aggregator_hidden_size', type=int, default=64,
                        help='dimensionality of hidden state of the rnn')
    parser.add_argument('--layers_before_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--layers_after_aggregator', nargs='+', type=int, default=[])
    parser.add_argument('--action_embedding_size', type=int, default=1)
    parser.add_argument('--state_embedding_size', type=int, default=32)
    parser.add_argument('--reward_embedding_size', type=int, default=8)

    # - decoder: rewards
    parser.add_argument('--decode_reward', type=boolean_argument, default=True, help='use reward decoder')
    parser.add_argument('--input_prev_state', type=boolean_argument, default=False, help='use prev state for rew pred')
    parser.add_argument('--input_action', type=boolean_argument, default=False, help='use prev action for rew pred')
    parser.add_argument('--reward_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--rew_pred_type', type=str, default='deterministic',
                        help='choose from: bernoulli, gaussian, deterministic')
    parser.add_argument('--multihead_for_reward', type=boolean_argument, default=False,
                        help='one head per reward pred (i.e. per state, default True)')
    parser.add_argument('--rew_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')

    # - decoder: state transitions
    parser.add_argument('--decode_state', type=boolean_argument, default=True, help='use state decoder(default False)')
    parser.add_argument('--state_loss_coeff', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--state_decoder_layers', nargs='+', type=int, default=[64, 32])
    parser.add_argument('--state_pred_type', type=str, default='deterministic',
                        help='choose from: deterministic, gaussian')

    # - decoder: ground-truth task ("metavim oracle", after Humplik et al. 2019)
    parser.add_argument('--decode_task', type=boolean_argument, default=False, help='use task decoder(default False)')
    parser.add_argument('--task_loss_coeff', type=float, default=1.0, help='weight for task loss (vs other losses)')
    parser.add_argument('--task_decoder_layers', nargs='+', type=int, default=[32, 32])
    parser.add_argument('--task_pred_type', type=str, default='task_id', help='choose from: task_id, task_description')

    # --- ABLATIONS ---

    parser.add_argument('--disable_decoder', type=boolean_argument, default=False)
    parser.add_argument('--disable_stochasticity_in_latent', type=boolean_argument, default=False)
    parser.add_argument('--sample_embeddings', type=boolean_argument, default=False,
                        help='sample the embedding (otherwise: pass mean)')
    parser.add_argument('--rlloss_through_encoder', type=boolean_argument, default=False,
                        help='backprop rl loss through encoder')
    parser.add_argument('--vae_loss_coeff', type=float, default=1.0, help='weight for VAE loss (vs RL loss)')
    parser.add_argument('--kl_to_gauss_prior', type=boolean_argument, default=False)
    parser.add_argument('--learn_prior', type=boolean_argument, default=False)
    parser.add_argument('--decode_only_past', type=boolean_argument, default=False,
                        help='whether to decode future observations')
    parser.add_argument('--condition_policy_on_state', type=boolean_argument, default=True,
                        help='after the encoder, add the env state to the latent space')

    # --- decoder: add neighbor
    parser.add_argument('--use_neighbor', type=boolean_argument, default=True, help='if use the info of the neighbor or not')
    parser.add_argument('--decode_state_neighbor', type=boolean_argument, default=True, help='use state decoder with action of neighbor')
    parser.add_argument('--decode_reward_neighbor', type=boolean_argument, default=True, help='use reward decoder with action of neighbor')
    parser.add_argument('--input_action_neighbor', type=boolean_argument, default=True, help='use action of neighbor for rew pred')
    parser.add_argument('--state_loss_coeff_neighbor', type=float, default=1.0, help='weight for state loss (vs reward loss)')
    parser.add_argument('--rew_loss_coeff_neighbor', type=float, default=1.0, help='weight for reward loss (vs state loss)')

    # --- intrinsic reward
    parser.add_argument('--use_intrinsic_reward', type=boolean_argument, default=True, help='use intrinsic reward or not (default False)')
    parser.add_argument('--intrinsic_reward_weight', type=float, default=-1.0, help='weight for intrinsic reward (should be minus number)')



    # --- OTHERS ---

    # logging, saving, evaluation
    parser.add_argument('--log_interval', type=int, default=1000,
                        help='log interval, one log per n updates (default: 500)')
    parser.add_argument('--save_interval', type=int, default=1000,
                        help='save interval, one save per n updates (default: 1000)')
    parser.add_argument('--eval_interval', type=int, default=1000,
                        help='eval interval, one eval per n updates (default: 1000)')
    parser.add_argument('--vis_interval', type=int, default=1000,
                        help='visualisation interval, one eval per n updates (default: None)')
    parser.add_argument('--agent_log_dir', default='.', help='directory to save agent logs (default: /tmp/gym)')
    parser.add_argument('--results_log_dir', default=None, help='directory to save agent logs (default: ./data)')

    # general settings
    parser.add_argument('--seed', type=int, default=73, help='random seed (default: 73)')
    parser.add_argument('--deterministic_execution', type=boolean_argument, default=False,
                        help='Make code fully deterministic. Expects 1 process and uses deterministic CUDNN')
    parser.add_argument('--num_processes', type=int, default=16,
                        help='how many training CPU processes to use (default: 16)')  # 16 9 attention
    parser.add_argument('--port', type=int, default=8097, help='port to run the server on (default: 8097)')

    # load model
    parser.add_argument('--policy_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSpolicy20.pt', help="policy model path")
    parser.add_argument('--encoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRS_encoder20.pt', help="encoder model path")
    parser.add_argument('--task_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/task_decoder_model20.pt', help="task_decoder_model model path")
    parser.add_argument('--reward_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder20.pt', help="reward_decoder model path")
    parser.add_argument('--reward_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSreward_decoder_neighbor20.pt', help="reward_decoder_neighbor model path")
    parser.add_argument('--state_decoder_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder20.pt', help="state_decoder model path")
    parser.add_argument('--state_decoder_neighbor_model', type=str, default='/datasets/cluster/zlw_cluster/transfer_model/MetaVRSstate_decoder_neighbor20.pt', help="state_decoder_neighbor model path")
    parser.add_argument('--test_policy_num_steps', type=int, default=3600,  # 60
                        help='number of env steps to do during test')

    parser.add_argument('--log_name', type=str, default='noname', help="log name under zlwlog folder")

    args = parser.parse_args()

    args.cuda = torch.cuda.is_available()

    return args